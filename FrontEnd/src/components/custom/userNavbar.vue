<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <a class="navbar-brand nav-element" href="/userHome">Grocery Store</a>
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="/myCart">My Cart</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/orders">My Orders</a>
          </li>
        </ul>
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
  </div>
</template>

<script>
import Cookies from 'js-cookie'
export default {
  name: 'user-navbar',
  methods: {
    onClickLogout() {
      Cookies.remove('logged_id')
      Cookies.remove('jwt_token')
      Cookies.remove('username')
      Cookies.remove('role')
      this.$router.push('/')
    },
  },
}
</script>

<style></style>
