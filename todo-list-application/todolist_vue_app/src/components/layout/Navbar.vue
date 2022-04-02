<template>
  <nav class="navbar is-dark">
    <div class="navbar-brand">
      <router-link to="/" class="navbar-item">
        <strong>Todo List</strong>
      </router-link>
    </div>
    <div class="navbar-menu">
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <template v-if="!$store.state.firebaseUser">
              <router-link :to="{ name: 'Register' }" class="button is-success"
                ><strong> Sign Up</strong></router-link
              >
              <router-link :to="{ name: 'Login' }" class="button is-light"> Log in </router-link>
            </template>
            <template v-else>
              <button @click="logout" class="button is-danger"><strong> Log Out </strong></button>
              <router-link :to="{ name: 'MyAccount' }" class="button is-info"> My Account </router-link>
            </template>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import firebase from "firebase";

export default {
  name: "Navbar",
  methods: {
    async logout() {
      await firebase
        .auth()
        .signOut()
        .then(() => {
          console.log("Logged out");
        })
        .catch(error => {
          console.loh("here");
          console.log(error);
        });
      this.$store.commit("removeUser");
      this.$router.push({ name: "Login" });
    }
  }
};
</script>
