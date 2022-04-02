<template>
  <div class="container">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Sign Up</h1>
        <form @submit.prevent="submitForm">
          <div class="field">
            <label for="">Email</label>
            <div class="control">
              <input type="email" name="email" class="input" v-model="email" />
            </div>
          </div>

          <div class="field">
            <label for="">username</label>
            <div class="control">
              <input type="text" name="username" class="input" v-model="username" />
            </div>
          </div>

          <div class="field">
            <label for="">First Name</label>
            <div class="control">
              <input type="text" name="firstName" class="input" v-model="firstName" />
            </div>
          </div>

          <div class="field">
            <label for="">Last Name</label>
            <div class="control">
              <input type="text" name="firstName" class="input" v-model="lastName" />
            </div>
          </div>

          <div class="field">
            <label for="">Password</label>
            <div class="control">
              <input type="password" name="password1" class="input" v-model="password1" />
            </div>
          </div>

          <div class="field">
            <label for="">Repeat password</label>
            <div class="control">
              <input type="password" name="password2" class="input" v-model="password2" />
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" :key="error">
              {{ error }}
            </p>
          </div>

          <div class="field">
            <div class="control">
              <button class="button is-success">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import firebase from "firebase/app";
import "firebase/auth";
import { toast } from "bulma-toast";
export default {
  name: "SignUp",

  data() {
    return {
      username: "",
      email: "",
      firstName: "",
      lastName: "",
      password1: "",
      password2: "",
      errors: []
    };
  },
  methods: {
    async submitForm() {
      this.errors = [];
      if (this.username === "") {
        this.errors.push("The username is missing");
      }
      if (!this.checkUsername(this.username)) {
        this.errors.push("Only '_' is allowed for special characters");
      }
      if (this.email === "") {
        this.errors.push("The email is missing");
      }
      if (this.firstName === "") {
        this.errors.push("The First Name is missing");
      }
      if (this.lastName === "") {
        this.errors.push("The First Name is missing");
      }
      if (this.password1 == "") {
        this.errors.push("This password is too short");
      }
      if (this.password1 !== this.password2) {
        this.errors.push("The passwords do not match");
      }
      if (!this.errors.length) {
        this.$store.commit("setIsLoading", true);
        // Create user on firebase
        await axios
          .get('api/v1/auth/check-duplicate-username/', { params: { username: this.username}})
          .then(async () => {
              await firebase
              .auth()
              .createUserWithEmailAndPassword(this.email, this.password1)
              .then(async () => {
                const user = firebase.auth().currentUser;
                // Save user username on firebase
                await user.updateProfile({
                  displayName: this.username
                });
                this.$store.commit("updateUser", user);
                const uid = user.uid;
                // Get New Access Token
                await user
                  .getIdToken(true)
                  .then(async token => {
                    axios.defaults.headers.common["Authorization"] = "Bearer " + token;
                    const data = {
                      first_name: this.firstName,
                      last_name: this.lastName,
                      uid,
                      username: this.username
                    };
                    // Add user roles to firebase server side

                    await axios
                      .post("api/v1/auth/firebase-user-created/", data)
                      .then(async () => {
                        // Create athelete user on database
                        this.$router.push({ name: "Home" });
                      })
                      .catch(err => {
                        console.log(error);
                      });
                  })
                  .catch(err => {
                    console.log(err);
                  });
              })
              .catch(error => {
                if (error.message) {
                  this.errors.push(error.message);
                } else if (error.response) {
                  console.log(error);
                  for (const property in error.response.data) {
                    console.log(`${property}: ${error.response.data[property]}`);
                  }
                  this.errors.push("Something went wrong. Please try again!");
                }
              });
          })
          .catch(()=> {
            this.errors.push("This username already exists");
          })

        this.$store.commit("setIsLoading", false);
      }
    },
    checkUsername(username) {
      const re = /^\w+$/;
      if (!re.test(username)) {
        return false;
      }
      return true;
    }
  }
};
</script>
