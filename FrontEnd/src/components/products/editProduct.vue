<template>
  <div class="content-wrapper">
    <managerNav />
    <div class="container mt-4">
      <div class="row d-flex justify-content-center">
        <div class="col-lg-6">
          <div class="card">
            <div class="card-body">
              <h3>Edit Product Section</h3>
              <h5>Please Enter Updated Product Details</h5>
              <form @submit.prevent="editProducts">
                <div v-if="flash_message" class="flash-message">
                  <h6 class="text-danger">{{ flash_message }}</h6>
                </div>
                <div class="form-group">
                  <label for="editProductName">Old Product Name:</label>
                  <input
                    v-model="editProductName"
                    type="text"
                    class="form-control"
                    id="editProductName"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="editNewProductName">New Product Name:</label>
                  <input
                    v-model="editNewProductName"
                    type="text"
                    class="form-control"
                    id="editNewProductName"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="categories">Choose Category:</label>
                  <select
                    class="form-control"
                    v-model="selectedCategory"
                    id="categories"
                  >
                    <option value="" disabled selected>Select Category</option>
                    <option
                      v-for="(category, index) in categories"
                      :value="category.category_id"
                      :key="index"
                    >
                      {{ category.category_name }}
                    </option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="editPrice">Product price:</label>
                  <input
                    v-model="editPrice"
                    type="text"
                    class="form-control"
                    id="editPrice"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="units">Select Units:</label>
                  <select
                    class="form-control"
                    v-model="selectedUnit"
                    id="units"
                  >
                    <option value="" disabled selected>Select Units</option>
                    <option value="litres">Litres</option>
                    <option value="kgs">Kgs</option>
                    <option value="dozens">Dozens</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="quantity">quantity</label>
                  <input
                    v-model="quantity"
                    type="number"
                    class="form-control"
                    id="quantity"
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
import managerNav from '../custom/managerNav'
import axios from 'axios'
import Cookies from 'js-cookie'

export default {
  name: 'addproduct-home',
  components: {
    managerNav,
  },
  data() {
    return {
      categories: [],
      editProductName: '',
      editNewProductName: '',
      editPrice: '',
      quantity: '',
      selectedCategory: '',
      selectedUnit: '',
      flash_message: '',
    }
  },
  mounted() {
    this.fetchCategories()
  },
  methods: {
    async fetchCategories() {
      //api call for fetching categories and storing in the categories list
      await axios
      try {
        const response = await axios.get('http://localhost:5050/getCategories')
        console.log(response)
        this.categories = response.data.categories
        console.log(this.categories)
      } catch (error) {
        console.log(error)
      }
    },
    async editProducts() {
      //api call for editing the products based on the old product name reference and can edit if the creator of the product and wanted to edit the product are same
      const logged_id = Cookies.get('logged_id')
      console.log(logged_id)
      const data = {
        editProductName: this.editProductName,
        editNewProductName: this.editNewProductName,
        editPrice: this.editPrice,
        quantity: this.quantity,
        category: this.selectedCategory,
        unit: this.selectedUnit,
        store_manager_id: logged_id,
      }
      await axios
      try {
        const response = await axios.post(
          'http://localhost:5050/editProduct',
          data,
        )
        console.log(response)
        if (response.request.status == 202 || response.request.status == 201) {
          this.flash_message = response.data.flash_message
        } else {
          this.$router.push('/managerHome')
        }
      } catch (error) {
        console.log(error)
      }
    },
  },
}
</script>
