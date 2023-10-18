<template>
  <div class="d-flex flex-column align-items-center justify-content-center p=5">
    <h1>Not Found URL or Unauthorized Access</h1>
    <p>Click the button to Go Home</p>
    <button @click="backHome" class="btn btn-warning" style="width: 100px">
      Go Home
    </button>
  </div>
</template>

<script>
import cookies from 'js-cookie'

export default {
  name: 'NotFound-page',
  methods: {
    backHome() {
      const role = cookies.get('role')
      if (role === 'admin') {
        this.$router.push('/adminHome')
      } else if (role === 'manager') {
        this.$router.push('/managerHome')
      } else if (role === 'user') {
        this.$router.push('/userHome')
      } else {
        this.$router.push('/')
      }
    },
  },
}
</script>
