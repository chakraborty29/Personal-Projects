<template>
  <div class="container">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->

    <div class="columns">
      <div class="column is-3 is-offset-3">
        <form action="">
          <h2 class="subtitle">Add task</h2>
          <h2 class="subtitle">{{ test }}</h2>

          <div class="field">
            <label class="label">Description</label>
            <div class="control">
              <input @change="validate" v-model="description" class="input" type="text" />
            </div>
          </div>

          <div class="field">
            <label class="label">Status</label>
            <div class="control">
              <div class="select">
                <select @change="validate" v-model="status">
                  <option value="todo">To do</option>
                  <option value="done">Done</option>
                </select>
              </div>
            </div>
          </div>

          <div v-if="errors.length > 0 && this.changed">
            <ul>
              <li v-for="error of errors" :key="error">{{ error }}</li>
            </ul>
          </div>

          <div class="field">
            <div class="control">
              <button :disabled="!valid" @click="submitForm" class="button is-link">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>
    <div class="columns">
      <div class="column is-6">
        <h2 class="subtitle">To do</h2>

        <div class="is-loading-bar has-text-centered" :class="{ 'is-loading': isLoading }">
          <div class="lds-dual-ring"></div>
        </div>

        <div class="todo">
          <div class="card" v-for="task in tasks" v-bind:key="task.id">
            <div v-if="task.status === 'todo'" class="card-content">{{ task.description }}</div>
            <footer v-if="task.status === 'todo'" class="card-footer">
              <a @click="todoDone(task.id)" class="card-footer-item">Done</a>
            </footer>
          </div>
        </div>
      </div>

      <div class="column is-6">
        <h2 class="subtitle">Done</h2>

        <div class="is-loading-bar has-text-centered" :class="{ 'is-loading': isLoading }">
          <div class="lds-dual-ring"></div>
        </div>
        <div class="todo">
          <div class="card" v-for="task in tasks" v-bind:key="task.id">
            <div style="text-decoration: line-through;" v-if="task.status === 'done'" class="card-content">{{ task.description }}</div>
            <footer v-if="task.status === 'done'" class="card-footer">
              <a @click="deleteTodo(task.id)" class="card-footer-item button is-danger">Delete</a>
            </footer>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions, mapGetters } from "vuex";

// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue';

export default {
  name: "Home",
  data() {
    return {
      test: "",
      description: '',
      status: '',
      valid: false,
      errors: [],
      isLoading: false,
    };
  },
  async created() {
    await this.updateToken();
    await this.getTasks();
  },
  mounted() {
    this.validate(true);
  },
  computed: {
    ...mapGetters(["getToken", "getFirebaseUser", "getTaskList"]),
    firebaseUser: {
      get() {
        return this.getFirebaseUser;
      },
      set(newValue) {
        return newValue;
      }
    },
    token: {
      get() {
        return this.getToken;
      }
    },
    tasks: {
      get() {
        return this.getTaskList;
      }
    }
  },
  methods: {
    ...mapActions(["updateToken", "pullTaskList", "postTasks", "deleteTask", "changeTaskStatus"]),
    validate(nochange) {
      if (nochange) {
        this.changed = false;
      } else {
        this.changed = true;
      }
      this.errors = [];
      if (this.description === '') {
        this.errors.push('Description can not be blank');
      }
      if (this.status === '') {
        this.errors.push('Status can not be blank');
      }
      if (this.errors.length > 0) {
        this.valid = false;
        return false;
      }
      this.valid = true;
      return true;
    },
    async getTasks() {
      this.isLoading =  true;
      await this.pullTaskList()
        .then(() => {
          this.isLoading =  false;
        })
        .catch((err) => {
          console.log(err);
        })
    },
    async submitForm() {
      await this.postTasks({ description: this.description, status: this.status})
      .then(async () => {
        await this.getTasks();
      })
      .catch((err) => {
        console.log(err);
      })
    },
    async todoDone(id) {
      await this.changeTaskStatus({ id })
      .then(async () => {
        await this.getTasks();
      })
      .catch((err) => {
        console.log(err);
      })
    },
    async deleteTodo(id) {
      await this.deleteTask({ id })
      .then(async () => {
        await this.getTasks();
      })
      .catch((err) => {
        console.log(err);
      })
    }
  }
  // components: {
  //   HelloWorld,
  // },
};
</script>
<style lang="scss">
.select,
select {
  width: 100%;
}

.card {
  margin-bottom: 20px;
}

.done {
  opacity: 0.3;
}
</style>
