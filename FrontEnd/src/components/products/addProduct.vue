<template>
  <div class="content-wrapper">
    <managerNav />
    <div class="container mt-4">
      <div class="row d-flex justify-content-center">
        <div class="col-lg-6">
          <div class="card">
            <div class="card-body">
              <h3>Add Product Section</h3>
              <h5>Please Enter Product Details</h5>
              <form @submit.prevent="addProducts">
                <div v-if="flash_message" class="flash-message">
                  <h6 class="text-danger">{{ flash_message }}</h6>
                </div>
                <div class="form-group">
                  <label for="productName">Product Name:</label>
                  <input
                    v-model="productName"
                    type="text"
                    class="form-control"
                    id="productName"
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
                  <label for="price">Product Price:</label>
                  <input
                    v-model="price"
                    type="text"
                    class="form-control"
                    id="price"
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
                    <option value="Litre">Litres</option>
                    <option value="Kg">Kg</option>
                    <option value="Dozen">Dozens</option>
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
  data() {
    return {
      categories: [],
      productName: '',
      price: '',
      quantity: '',
      selectedUnit: '',
      selectedCategory: '',
      flash_message: '',
    }
  },
  components: {
    managerNav,
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
    async addProducts() {
      //api call for adding  products and storing in the database sending data post request
      const logged_id = Cookies.get('logged_id')
      console.log(logged_id)
      const data = {
        productName: this.productName,
        price: this.price,
        quantity: this.quantity,
        category: this.selectedCategory,
        units: this.selectedUnit,
        store_manager_id: logged_id,
      }

      await axios
      try {
        const response = await axios.post(
          'http://localhost:5050/addProduct',
          data,
        )
        console.log(response)
        if (response.request.status == 202) {
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
