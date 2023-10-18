<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title text-center">Login</h2>
            <div v-if="flash_message" class="flash-message">
              <h6 class="text-danger">{{ flash_message }}</h6>
            </div>
            <form @submit.prevent="login">
              <div class="form-group">
                <label for="username">Username</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="username"
                  required
                />
              </div>
              <div class="form-group">
                <label for="password">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="password"
                  required
                />
              </div>
              <p>Select your role:</p>
              <label v-for="role in Roles" :key="role.value">
                <input
                  type="radio"
                  :value="role.value"
                  v-model="selectedRole"
                />
                {{ role.label }}
                &nbsp;
              </label>
              <div class="my-4">
                <button type="submit" class="btn btn-primary btn-block">
                  Login
                </button>
              </div>
            </form>
            <a href="/signup" class="text-decoration-none"
              >Don't have an account <span>Sign Up</span></a
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'
export default {
  name: 'login-page',
  data() {
    return {
      username: '',
      password: '',
      selectedRole: '',
      loginId: '',
      Roles: [
        {label: 'Admin', value: 'admin'},
        {label: 'Manager', value: 'manager'},
        {label: 'User', value: 'user'},
      ],
      flash_message: null,
    }
  },
  methods: {
    async login() {
      const data = {
        username: this.username,
        password: this.password,
        role: this.selectedRole,
      }
      axios
        .post('http://localhost:5050/login', data)
        .then(response => {
          console.log(response)
          if (response.request.status == 200) {
            this.flash_message = response.data.flash_message
          } else if (response.request.status == 201) {
            const token = response.data.token
            const role = response.data.role
            Cookies.set('jwt_token', token, {expires: 1})
            const Hello2 = Cookies.get('jwt_token')
            console.log(Hello2)
            if (role == 'manager' || role == 'user')
              Cookies.set('logged_id', response.data.id, {expires: 1})
            Cookies.set('username', response.data.username, {expires: 1})
            Cookies.set('role', role, {expires: 1})
            const hello = Cookies.get('logged_id')
            console.log(hello)
            if (role == 'admin') this.$router.push('/adminHome')
            else if (role == 'manager') this.$router.push('/managerHome')
            else this.$router.push('/userHome')
          } else {
            this.flash_message = response.data.flash_message
          }
        })
        .catch(error => {
          console.log(error)
          console.error('Login failed:')
        })
    },
  },
}
</script>

<style></style>
