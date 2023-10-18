<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <a class="navbar-brand nav-element" href="/managerHome">Grocery Store</a>
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
            Product Management
          </a>
          <div class="dropdown-menu" aria-labelledby="categoryDropdown">
            <router-link to="/addProduct">
              <a class="dropdown-item" href="#">Add Product</a>
            </router-link>
            <router-link to="/editProduct">
              <a class="dropdown-item" href="#">Edit Product</a>
            </router-link>

            <router-link to="/deleteProduct">
              <a class="dropdown-item" href="#"> Remove Product</a>
            </router-link>
          </div>
        </li>
      </ul>

      <button class="btn btn-warning" @click="csv_downloader">
        Download Report
      </button>

      <ul class="navbar-nav ml-auto">
        <li>
          <button
            class="btn btn-outline-danger my-2 my-sm-0"
            @click="onClickLogout"
          >
            Logout
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import Cookies from 'js-cookie'
import axios from 'axios'
export default {
  name: 'manager-navbar',
  data() {
    return {
      store_manager_id: Cookies.get('logged_id'),
    }
  },
  methods: {
    onClickLogout() {
      Cookies.remove('logged_id')
      Cookies.remove('jwt_token')
      Cookies.remove('username')
      Cookies.remove('role')
      this.$router.push('/')
    },
    async csv_downloader() {
      //api call for downloading products  and storing in the csv list
      console.log('Helloworld')
      const user_id = this.store_manager_id
      console.log(this.store_manager_id)
      try {
        const response = await axios.get(
          `http://localhost:5050/export_products/${user_id}`,
        )
        console.log(response)
      } catch (error) {
        console.log(error)
      }
    },
  },
}
</script>
