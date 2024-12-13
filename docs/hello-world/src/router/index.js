import { createRouter, createWebHistory } from 'vue-router';
import HomePageLayout from '../components/HomePageLayout.vue';
import CodeforcesLayout from '../components/CodeforcesLayout.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePageLayout
  },
  {
    path: '/codeforces',
    name: 'Codeforces',
    component: CodeforcesLayout
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
