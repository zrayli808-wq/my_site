import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AlbumDetailView from '../views/AlbumDetailView.vue'
import DesignView from '../views/DesignView.vue'
import MusicView from '../views/MusicView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/design', name: 'design', component: DesignView },
  { path: '/music', name: 'music', component: MusicView },
  { path: '/album/:id', name: 'album-detail', component: AlbumDetailView, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router