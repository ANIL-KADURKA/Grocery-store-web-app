<template>
  <div class="content-wrapper">
    <managerNav />
    <div class="container-xxl flex-grow-1 container-p-y mt-5">
      <div class="row d-flex justify-content-center">
        <div v-if="flash_message" class="flash-message">
          <h6 class="text-danger text-center">{{ flash_message }}</h6>
        </div>
        <div class="col-lg-6">
          <div class="card">
            <div class="card-body">
              <h4>All Products Section</h4>
              <div class="d-flex flex-row justify-content-between">
                <div class="mr-4">Product Name</div>
                <div>Price</div>
                <div class="mr-3">No of Items</div>
                <div class="mr-3">Delete status</div>
              </div>
              <ul class="list-group">
                <li
                  v-for="(product, index) in products"
                  :key="index"
                  class="list-group-item"
                >
                  <div class="d-flex justify-content-between">
                    <div>{{ product.product_name }}</div>
                    <div>
                      <button class="btn btn-warning btn-block">
                        {{ product.price }} /- {{ product.units }}
                      </button>
                    </div>
                    <div>
                      <div v-if="product.Quantity > 0">
                        <p class="text-success">{{ product.Quantity }} Items</p>
                      </div>
                      <div v-else>
                        <p class="text-danger">Out of Stock</p>
                      </div>
                    </div>
                    <div>
                      <button
                        @click="setDeleteProduct(product.product_name)"
                        class="btn btn-danger btn-block"
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
import managerNav from '../custom/managerNav'
import axios from 'axios'
export default {
  name: 'manager-home',
  data() {
    return {
      products: [],
      flash_message: null,
    }
  },
  components: {
    managerNav,
  },
  mounted() {
    this.fetchProducts()
  },
  methods: {
    async fetchProducts() {
      //api call for fetching products and storing in the products list
      await axios
      try {
        const response = await axios.get('http://localhost:5050/allproducts')
        console.log(response)
        this.products = response.data.products
        console.log(this.products)
      } catch (error) {
        console.log(error)
      }
    },
    async setDeleteProduct(product_name) {
      //api call for setting the status="delete" so that it goes for confirmation to the admin to delete product
      await axios
        .post('http://localhost:5050/setDeleteProduct', {
          product_name: product_name,
        })
        .then(response => {
          console.log(response.data.message)
          this.flash_message = response.data.message
          this.fetchProducts()
        })
        .catch(error => {
          console.error(error)
        })
    },
  },
}
</script>
