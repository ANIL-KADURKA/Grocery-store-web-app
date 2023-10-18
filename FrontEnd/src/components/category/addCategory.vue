<template>
  <div class="content-wrapper">
    <navbar />
    <div class="container mt-4">
      <div class="row d-flex justify-content-center">
        <div class="col-lg-6">
          <div class="card">
            <div class="card-body">
              <h3>Add Category Section</h3>
              <h5>Please Enter Category Details</h5>
              <form @submit.prevent="addCategory">
                <div class="form-group">
                  <label for="categoryName">Category Name:</label>
                  <input
                    v-model="categoryName"
                    type="text"
                    class="form-control"
                    id="categoryName"
                    required
                  />
                </div>
                <button type="submit" class="btn btn-primary mt-3">
                  Submit
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import navbar from '../custom/navbar.vue' 
import axios from 'axios'
export default {
  name: 'add-category',
  components: {
    navbar,
  },
  data() {
    return {
      categoryName: '',
    }
  },
  methods: {
    async addCategory() {
      //api call for adding category and storing in db
      const data = {
        categoryName: this.categoryName,
      }
      axios
        .post('http://localhost:5050/add_category', data)
        .then(response => {
          console.log(response)
          this.$router.push('/adminHome')
        })
        .catch(error => {
          console.error('Adding failed:', error)
        })
    },
  },
}
</script>
