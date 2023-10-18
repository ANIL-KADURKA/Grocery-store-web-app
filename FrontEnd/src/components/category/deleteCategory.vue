<template>
  <div class="content-wrapper">
    <navbar />
    <div class="container-xxl flex-grow-1 container-p-y mt-5">
      <div class="row d-flex justify-content-center">
        <div class="col-lg-6">
          <div class="card">
            <div class="card-body">
              <h4>Delete Category</h4>
              <ul class="list-group">
                <li
                  v-for="(category, index) in categories"
                  :key="index"
                  class="list-group-item"
                >
                  <div class="d-flex justify-content-between">
                    <div>{{ category.category_name }}</div>
                    <div>
                      <button
                        class="btn btn-danger btn-block"
                        @click="deleteCategory(category.category_id)"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </li>
              </ul>
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
  name: 'delete-category',
  components: {
    navbar,
  },
  data() {
    return {
      categories: [],
    }
  },
  mounted() {
    this.fetchCategories()
  },
  methods: {
    async fetchCategories() {
      try {
        //api call for fetching categories and storing in the categories list
        const response = await axios.get('http://localhost:5050/getCategories')
        console.log(response)
        this.categories = response.data.categories
        console.log(this.categories)
      } catch (error) {
        console.error(error)
      }
    },
    async deleteCategory(categoryId) {
      //api call for deleting category permanently from the db
      await axios
        .post('http://localhost:5050/deleteCategory', {id: categoryId})
        .then(response => {
          console.log(response.data.message)
          this.fetchCategories()
        })
        .catch(error => {
          console.error(error)
        })
    },
  },
}
</script>
