import axios from 'axios';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import firebase from 'firebase';
import './config/firebaseSettings/firebaseInit';

// axios configuration
axios.defaults.baseURL = process.env.VUE_APP_API_URL;

// firebase auth check
firebase.getCurrentUser = () => {
    return new Promise((resolve, reject) => {
      const unsubscribe = firebase.auth().onAuthStateChanged(user => {
        unsubscribe();
        resolve(user);
      }, reject);
    }
  )};

createApp(App).use(store).use(router, axios).use(firebase).mount('#app');
