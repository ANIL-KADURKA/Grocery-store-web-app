import {createRouter, createWebHistory} from 'vue-router'
import Cookies from 'js-cookie'

import login from './components/login.vue'
import signup from './components/signup.vue'
import adminHome from './components/adminHome.vue'
import addCategory from './components/category/addCategory.vue'
import deleteCategory from './components/category/deleteCategory.vue'
import editCategory from './components/category/editCategory.vue'
import managerHome from './components/manager/managerHome.vue'
import addProduct from './components/products/addProduct.vue'
import deleteProduct from './components/products/deleteProduct.vue'
import editProduct from './components/products/editProduct.vue'
import allProducts from './components/products/allProducts.vue'
import userHome from './components/userHome.vue'
import userCart from './components/userCart.vue'
import notFound from './components/notFound.vue'
import myorders from './components/myorders.vue'

const routes = [
  {
    path: '/',
    component: login, //login route avaialble to the all roles
  },
  {
    path: '/signup',
    component: signup, //signup route avaialble to the all roles
  },
  {
    path: '/adminHome',
    component: adminHome,
    meta: {roleAccessed: ['admin']}, // Only 'admin' role is allowed
  },
  {
    path: '/deleteCategory',
    component: deleteCategory,
    meta: {roleAccessed: ['admin']}, // Only 'admin' role is allowed
  },
  {
    path: '/addCategory',
    component: addCategory,
    meta: {roleAccessed: ['admin']},// Only 'admin' role is allowed
  },
  {
    path: '/editCategory',
    component: editCategory,
    meta: {roleAccessed: ['admin']},// Only 'admin' role is allowed
  },
  {
    path: '/managerHome',
    component: managerHome,
    meta: {roleAccessed: ['manager']},// Only 'manager' role is allowed
  },
  {
    path: '/deleteProduct',
    component: deleteProduct,
    meta: {roleAccessed: ['manager']},// Only 'manager' role is allowed
  },
  {
    path: '/addProduct',
    component: addProduct,
    meta: {roleAccessed: ['manager']},// Only 'manager' role is allowed
  },
  {
    path: '/editProduct',
    component: editProduct,
    meta: {roleAccessed: ['manager']},// Only 'manager' role is allowed
  },
  {
    path: '/allProducts',
    component: allProducts,
    meta: {roleAccessed: ['admin']},// Only 'admin' role is allowed
  },
  {
    path: '/userHome',
    component: userHome,
    meta: {roleAccessed: ['user']},// Only 'user' role is allowed
  },
  {
    path: '/myCart',
    component: userCart,
    meta: {roleAccessed: ['user']},// Only 'user' role is allowed
  },
  {
    path: '/notFound', //notFound route avaialble to the all roles
    component: notFound,
  },
  {
    path: '/orders',
    component: myorders,
    meta: {roleAccessed: ['user']},// Only 'user' role is allowed
  },
  {
    path: '/:catchAll(.*)',  //used like else to maintain the route that redirects directly to the notfound route
    redirect: '/notFound',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const requiredRole = to.meta.roleAccessed //using the middle ware meta  function for role based access
  const userRole = Cookies.get('role') //used to get the role from the Cookies 

  if (!requiredRole || requiredRole.includes(userRole)) {
    console.log('HElloworld')
    next() //going to the next path
  } else {
    next('/notFound') //redrected to the notfound url there the button is clickable makes it to the redirected on role based
  }
})

export default router //router is imported to use in main.js
