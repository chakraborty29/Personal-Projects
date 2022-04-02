<template>
  <div class="container">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Log In</h1>
        <form @submit.prevent="submitForm">
          <div class="field">
            <label for="">Email</label>
            <div class="control">
              <input type="text" name="email" class="input" v-model="email" />
            </div>
          </div>

          <div class="field">
            <label for="">Password</label>
            <div class="control">
              <input type="password" name="password" class="input" v-model="password" />
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
import firebase from "firebase";
// import axios from 'axios';
// import {toast} from 'bulma-toast'
export default {
  name: "Login",
  data() {
    return {
      email: "",
      password1: "",
      errors: []
    };
  },
  methods: {
    async submitForm() {
      this.errors = [];
      if (this.email === "") {
        this.errors.push("The email is missing");
      }
      if (this.password == "") {
        this.errors.push("This password is too short");
      }
      if (!this.errors.length) {
        this.$store.commit("setIsLoading", true);
        await firebase
          .auth()
          .signInWithEmailAndPassword(this.email, this.password)
          .then(res => {
            const user = res.user;
            this.$store.commit("updateUser", user);
            const username = user.displayName;
            this.$router.push({ name: "Home" });
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
        this.$store.commit("setIsLoading", false);
      }
    }
  }
};
</script>
