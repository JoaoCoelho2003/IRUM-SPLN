import { createRouter, createWebHistory } from "vue-router"
import Home from "../views/HomeView.vue"
import Search from "../views/SearchView.vue"
import Document from "../views/DocumentView.vue"
import Browse from "../views/BrowseView.vue"

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/search",
    name: "Search",
    component: Search,
  },
  {
    path: '/document/:id(.*)',
    name: "Document",
    component: Document,
    props: true,
  },
  {
    path: "/browse",
    name: "Browse",
    component: Browse,
  },
]

const router = createRouter({
  history: createWebHistory("/"),
  routes,
})

export default router
