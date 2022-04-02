<template>
  <div>
    <template v-if="!this.$store.state.isAuthenticated && !navigation && !this.$store.state.isLoading && !this.$store.state.token">
      <div class="is-loading-bar has-text-centered is-loading">
        <div class="lds-dual-ring"></div>
      </div>
    </template>
    <template v-else>
      <Navbar />
      <div class="is-loading-bar has-text-centered" :class="{ 'is-loading': this.$store.state.isLoading }">
        <div class="lds-dual-ring"></div>
      </div>
    </template>
    <!-- <p v-if="this.$store.state.isAuthenticated">{{ this.$store.state.token }}</p> -->
    <router-view :key="$route.fullPath"/>
  </div>
</template>

<script>
import firebase from 'firebase/app';
import 'firebase/auth';
import Navbar from '@/components/layout/Navbar.vue';

export default {
  name: 'App',
  components: {
    Navbar,
  },
  data() {
    return {
      navigation: null,
    };
  },
  async created() {
    console.log(1)
    const user = await firebase.getCurrentUser();
    console.log(2)
    this.$store.commit("updateUser", user);
    console.log(3)
  },
  methods: {
    checkRoute() {
      if (this.$route.name === "Login" || this.$route.name === "Register" || this.$route.name === "ForgotPassword") {
        this.navigation = true;
        return;
      }
      this.navigation = false;
    },
  },
  watch: {
    $route() {
      this.checkRoute();
    },
  },
};
</script>

<style lang="scss">
@import '../node_modules/bulma';

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.is-loading-bar {
  height: 0;
  overflow: hidden;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
  &.is-loading {
    height: 80px;
  }
}
// #app {
//   font-family: Avenir, Helvetica, Arial, sans-serif;
//   -webkit-font-smoothing: antialiased;
//   -moz-osx-font-smoothing: grayscale;
//   text-align: center;
//   color: #2c3e50;
// }

// #nav {
//   padding: 30px;

//   a {
//     font-weight: bold;
//     color: #2c3e50;

//     &.router-link-exact-active {
//       color: #42b983;
//     }
//   }
// }
</style>
