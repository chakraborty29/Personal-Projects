import { createRouter, createWebHistory } from 'vue-router';
import firebase from 'firebase';
import Home from '../views/Home.vue';
import About from '../views/About.vue';
import SignUp from '../views/authentication/Signup.vue';
import Login from '../views/authentication/Login.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/profile',
    name: 'MyAccount',
    component: About
  },
  {
    path: "/signup",
    name: "Register",
    component: SignUp,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requireAdminOrStaff = to.matched.some(record => record.meta.requireAdminOrStaff);
  const user = await firebase.getCurrentUser()

  if (user) {
    user.getIdTokenResult()
      .then((token) => {
        if (requireAdminOrStaff) {
          if (!(token.claims.is_superuser || token.claims.is_staff)) {
            next('/')
          } else {
            next()
          }
        } else if (to.matched.some((res) => res.name === 'Login' || res.name === 'Register')) {
          next('/')
        } else {
          next()
        }
      })
  } else {
    if (requiresAuth) {
      next({ name: 'Login' })
    } else {
      next()
    }
  }
})

export default router;
