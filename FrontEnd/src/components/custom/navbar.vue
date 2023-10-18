<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <a class="navbar-brand nav-element" href="/adminHome">Grocery Store</a>
      <ul class="navbar-nav">
        <li class="nav-item dropdown">
          <a
            class="nav-link dropdown-toggle"
            href="#"
            id="categoryDropdown"
            role="button"
            data-bs-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
          >
            Category Management
          </a>
          <div class="dropdown-menu" aria-labelledby="categoryDropdown">
            <router-link to="/addCategory">
              <a class="dropdown-item" href="#">Add Category</a>
            </router-link>
            <router-link to="/editCategory">
              <a class="dropdown-item" href="#">Edit Category</a>
            </router-link>
            <router-link to="/deleteCategory">
              <a class="dropdown-item" href="#">Delete Categories</a>
            </router-link>
          </div>
        </li>
      </ul>
      <ul class="navbar-nav ml-auto">
        <li>
          <router-link to="/allproducts">
            <a href="#"
              ><button class="btn btn-outline-info my-2 my-sm-0">
                All Products
              </button></a
            >
          </router-link>
        </li>
      </ul>
      <ul class="navbar-nav ml-auto">
        <li>
          <button class="btn btn-outline-danger my-2 my-sm-0" @click="logout">
            Logout
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>
<script>
import Cookies from 'js-cookie'
export default {
  name: 'custom-navbar',
  data() {
    return {}
  },
  methods: {
    logout() {
      Cookies.remove('jwt_token')
      Cookies.remove('logged_id')
      Cookies.remove('username')
      Cookies.remove('role')
      this.$router.push('/')
    },
  },
}
</script>
