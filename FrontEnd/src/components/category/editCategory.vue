<template>
  <div class="content-wrapper">
    <navbar />
    <div class="container mt-4">
      <div class="row d-flex justify-content-center">
        <div class="col-lg-6">
          <div class="card">
            <div class="card-body">
              <h3>Edit Category Section</h3>
              <h5>Please Enter Category Details</h5>
              <form @submit.prevent="editCategory">
                <div class="form-group">
                  <label for="OldName">Please Enter Old Category Name:</label>
                  <input
                    v-model="oldName"
                    type="text"
                    class="form-control"
                    id="oldName"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="newName">Please Enter New Category Name:</label>
                  <input
                    v-model="newName"
                    type="text"
                    class="form-control"
                    id="newName"
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
  name: 'edit-category',
  components: {
    navbar,
  },
  data() {
    return {
      oldName: '',
      newName: '',
    }
  },
  methods: {
    async editCategory() {
      //api call for editing category based on old categoryName and updating the db
      const data = {
        oldName: this.oldName,
        newName: this.newName,
      }
      axios
        .post('http://localhost:5050/edit_category', data)
        .then(response => {
          console.log(response)
        })
        .catch(error => {
          console.error('Adding failed:', error)
        })
    },
  },
}
</script>
