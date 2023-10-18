<template>
  <div class="content-wrapper">
    <navbar />
    <div class="container-xxl flex-grow-1 container-p-y mt-5">
      <div class="row d-flex justify-content-center">
        <div class="col-lg-6">
          <div class="card">
            <div class="card-body">
              <h4>All Products Section</h4>
              <div class="d-flex flex-row justify-content-between">
                <div class="mr-4">Product Name</div>
                <div>Price</div>
                <div class="mr-3">No of Items</div>
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
                      <p class="text-warning">
                        {{ product.price }} Rs/- {{ product.units }}
                      </p>
                    </div>
                    <div>
                      <div v-if="product.Quantity > 0">
                        <p class="text-success">
                          {{ product.Quantity }} {{ product.units }}
                        </p>
                      </div>
                      <div v-else>
                        <p class="text-danger">Out of Stock</p>
                      </div>
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
  name: 'custom-navbar',
  data() {
    return {
      products: [],
    }
  },
  components: {
    navbar,
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
  },
}
</script>
