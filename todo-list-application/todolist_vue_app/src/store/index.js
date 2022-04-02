import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    // Auth States
    isLoading: false,
    isAuthenticated: false,
    token: '',
    firebaseUser: null,

    // Task states
    taskList: [],
  },
  mutations: {
    // Auth mutations
    setIsLoading(state, status) {
      state.isLoading = status;
    },
    updateUser(state, payload) {
      state.firebaseUser = payload;
      state.isAuthenticated = true;
    },
    setToken(state, payload) {
      state.token = payload;
      axios.defaults.headers.common['Authorization'] = "Bearer " + state.token;
      state.isAuthenticated = true;
    },
    removeUser(state) {
      state.isAuthenticated = false;
      state.token = '';
      state.userRole = null;
      state.firebaseUser = null;
    },

    // Task mutations
    setTaskList(state, payload) {
      state.taskList = payload;
    }
  },
  actions: {
    // Auth actions
    async updateToken({ commit, getters }) {
      const user = getters.getFirebaseUser;
      await user.getIdToken(true)
        .then((token) => {
          commit('setToken', token)
        })
        .catch((error) => {
            console.log(error);
        })
    },

    // Task actions
    pullTaskList({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get("api/v1/tasks/")
        .then(res => {
          commit("setTaskList", res.data)
          resolve(res.data);
        })
        .catch(err => {
          console.log(err);
          reject(err);
        });
      })
    },
    postTasks({ commit }, data) {
      return new Promise((resolve, reject) => {
        axios.post('api/v1/tasks/', data)
        .then((res) => {
          resolve(res.data)
        })
        .catch((err) => {
          console.log(err);
          reject(err);
        })
      })
    },
    changeTaskStatus({ commit }, data) {
      const { id } = data;
      return new Promise((resolve, reject) => {
        axios.patch(`api/v1/tasks/${id}/`, { status: 'done' })
        .then((res) => {
          resolve(res.data);
        })
        .catch((err) => {
          console.log(err);
          reject(err);
        })
      })
    },
    deleteTask({ commit }, data) {
      const { id } = data;
      return new Promise((resolve, reject) => {
        axios.delete(`api/v1/tasks/${id}/`)
        .then((res) => {
          resolve(res.data);
        })
        .catch((err) => {
          console.log(err);
          reject(err);
        })
      })
    },
  },
  getters: {
    // Auth getters
    getToken(state) {
      return state.token;
    },
    getFirebaseUser(state) {
      return state.firebaseUser;
    },

    // Task getters
    getTaskList(state) {
      return state.taskList;
    }
  },
});
