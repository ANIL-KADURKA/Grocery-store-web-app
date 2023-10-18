<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title text-center">User Registration Form</h2>
            <h6 v-if="flash_message" class="text-danger">
              {{ flash_message }}
            </h6>
            <div>
              <form @submit.prevent="signup">
                <div class="form-group">
                  <label for="name">Full Name</label>
                  <input
                    type="text"
                    class="form-control"
                    id="name"
                    v-model="name"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="email">Email</label>
                  <input
                    type="text"
                    class="form-control"
                    id="email"
                    v-model="email"
                    required
                  />
                </div>
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
                  {{ role.role }}
                  &nbsp;
                </label>
                <div class="my-4">
                  <button type="submit" class="btn btn-primary btn-block">
                    Signup
                  </button>
                </div>
              </form>
              <a href="/" class="text-decoration-none"
                >Have an account <span>Login ?</span></a
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'signup-page',
  data() {
    return {
      name: '',
      username: '',
      password: '',
      selectedRole: '',
      email: '',
      Roles: [
        {role: 'Manager', value: 'manager'},
        {role: 'User', value: 'user'},
      ],
      flash_message: null,
    }
  },
  methods: {
    async signup() {
      //api call for sending details signinup storing username password role in the db
      const data = {
        name: this.name,
        username: this.username,
        password: this.password,
        role: this.selectedRole,
        email: this.email,
      }
      axios
        .post('http://localhost:5050/signup', data)
        .then(response => {
          console.log(response)
          if (response.request.status == 200) {
            this.flash_message = response.data.flash_message
          } else {
            // const token = response.data.token
            // Cookies.set('jwt_token', token, {expires: 1})
            this.$router.push('/')
          }
        })
        .catch(error => {
          console.error('Login failed:', error)
        })
    },
  },
}
</script>
