<template>
  <div class="content-wrapper">
    <navbar />
    <div class="container-xxl flex-grow-1 container-p-y mt-5">
      <div class="row d-flex justify-content-center">
        <h1 class="text-center">Welcome {{ username }}</h1>

        <div class="col-lg-5">
          <div class="card">
            <div v-if="flash_message" class="card-header">
              <p>Add Product Manager</p>
              <p class="text-danger">{{ flash_message }}</p>
            </div>
            <div v-else class="card-header">
              <p>Add Product Manager</p>

              <div class="card-body">
                <div class="row">
                  <div class="col-lg-4">Full Name</div>
                  <div class="col-lg-4">Username</div>
                  <div class="col-lg-4">Approve Status</div>
                </div>
                <ul class="list-group">
                  <li
                    v-for="(manager, index) in storeManagers"
                    :key="index"
                    class="list-group-item"
                  >
                    <div class="row">
                      <div class="col-lg-4">{{ manager.name }}</div>
                      <div class="col-lg-3">{{ manager.username }}</div>
                      <div class="col-lg-5">
                        <div class="row">
                          <div class="col-lg-6">
                            <button
                              class="btn btn-primary btn-block"
                              @click="acceptCredentials(manager.id)"
                            >
                              Approve
                            </button>
                          </div>
                          <div class="col-lg-6">
                            <button
                              class="btn btn-danger btn-block"
                              @click="rejectCredentials(manager.id)"
                            >
                              Reject
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-6">
          <div class="card">
            <div v-if="flash_message2" class="card-header">
              <p>Delete Product</p>
              <p class="text-danger">{{ flash_message2 }}</p>
            </div>
            <div v-else class="card-body">
              <p>Delete Product</p>
              <div class="row">
                <div class="col-lg-3">Product</div>
                <div class="col-lg-3">Category</div>
                <div class="col-lg-2">Manager</div>
                <div class="col-lg-2">Delete</div>
                <div class="col-lg-2">Reject</div>
              </div>
              <ul class="list-group">
                <li
                  v-for="(product, index) in deleteProducts"
                  :key="index"
                  class="list-group-item"
                >
                  <div class="row">
                    <div class="col-lg-3">{{ product.product_name }}</div>
                    <div class="col-lg-3">{{ product.category_name }}</div>
                    <div class="col-lg-2">{{ product.manager_name }}</div>
                    <div class="col-lg-2">
                      <button
                        class="btn btn-primary btn-block"
                        @click="deleteProduct(product.product_id)"
                      >
                        Delete
                      </button>
                    </div>
                    <div class="col-lg-2">
                      <button
                        class="btn btn-danger btn-block"
                        @click="undeleteProduct(product.product_id)"
                      >
                        Reject
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
  <div class="container-xxl flex-grow-1 container-p-y mt-5">
    <div class="row d-flex justify-content-center">
      <div class="col-lg-6">
        <div class="card">
          <div class="card-body">
            <h4>Recent Categories Added Section</h4>
            <div class="d-flex flex-row justify-content-between">
              <div class="mr-4">Category Name</div>
              <div class="mr-4">Product Name</div>
              <div>Price</div>
              <div class="mr-3">No of products</div>
            </div>
            <ul class="list-group">
              <li
                v-for="(category_product, index) in category_products"
                :key="index"
                class="list-group-item"
              >
                <div class="d-flex justify-content-between">
                  <div>{{ category_product.category_name }}</div>
                  <div>{{ category_product.product_name }}</div>
                  <div>
                    <p class="text-warning">
                      {{ category_product.price }} /-
                      {{ category_product.units }}
                    </p>
                  </div>
                  <div>
                    <div v-if="category_product.Quantity > 0">
                      <p class="text-success">
                        {{ category_product.Quantity }}
                        {{ category_product.units }}
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
</template>

<script>
import axios from 'axios'
import navbar from './custom/navbar.vue'
import Cookies from 'js-cookie'
export default {
  name: 'admin-home',
  components: {
    navbar,
  },
  data() {
    return {
      storeManagers: [],
      deleteProducts: [],
      categories: [],
      category_products: [],
      username: Cookies.get('username'),
      flash_message: null,
      flash_message2: null,
    }
  },
  mounted() {
    this.fetchStoreManagers()
    this.fetchDeleteProducts()
    this.fetchCategories()
    this.fetchCategoriesWithProducts()
  },
  methods: {
    async fetchCategoriesWithProducts() {
      //api call for fetching categories and products  and storing in the category_products list
      try {
        const response = await axios.get(
          'http://localhost:5050/getcategories_products',
        )
        console.log(response)
        this.category_products = response.data.category_products
        console.log(this.category_products)
      } catch (error) {
        console.log(error)
      }
    },
    async fetchStoreManagers() {
      //api call for fetching store managers who are requested for apporvals and stored in storeManagers list
      try {
        const response = await axios.get('http://localhost:5050/store_requests')
        console.log(response)
        if (response.request.status == 202) {
          // console.log(response);
          this.storeManagers = response.data.storemanagers
          console.log(this.storeManagers)
        } else {
          this.flash_message = response.data.message
        }
      } catch (error) {
        console.error(error)
      }
    },
    async fetchDeleteProducts() {
      //api call for fetching products that i want to delete and storing in the deleteProducts list
      try {
        const res = await axios.get('http://localhost:5050/deleteProducts')
        console.log(res)
        if (res.request.status == 201) {
          // console.log(res);
          this.deleteProducts = res.data.deleteProducts
          console.log(this.deleteProducts)
        } else {
          this.flash_message2 = res.data.message
        }
      } catch (error) {
        console.error(error)
      }
    },

    async fetchCategories() {
      //api call for fetching categories and storing in the categories list
      try {
        const response = await axios.get('http://localhost:5050/getCategories')
        console.log(response)
        this.categories = response.data.categories
        console.log(this.categories)
      } catch (error) {
        console.error(error)
      }
    },
    acceptCredentials(userId) {
      //api call for accepting credentials of StoreManager and status updating in db  based on userId
      axios
        .post('http://localhost:5050/accept', {id: userId})
        .then(response => {
          console.log(response.data.message)
          this.fetchStoreManagers()
        })
        .catch(error => {
          console.error(error)
        })
    },
    rejectCredentials(userId) {
      //api call for rejecting credentials of StoreManager and removing it completely from db based on userId
      axios
        .post('http://localhost:5050/reject', {id: userId})
        .then(response => {
          console.log(response.data.message)
          this.fetchStoreManagers()
        })
        .catch(error => {
          console.error(error)
        })
    },
    deleteProduct(productId) {
      //api call for deleting the product completely from database using productId
      axios
        .post('http://localhost:5050/deleteProduct', {id: productId})
        .then(response => {
          console.log(response.data.message)
          this.fetchDeleteProducts()
        })
        .catch(error => {
          console.error(error)
        })
    },
    undeleteProduct(productId) {
      //api call for deleting the product completely from database using productId
      axios
        .post('http://localhost:5050/undeleteProduct', {id: productId})
        .then(response => {
          console.log(response.data.message)
          this.fetchDeleteProducts()
        })
        .catch(error => {
          console.error(error)
        })
    },
  },
}
</script>

<style>
.category-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  padding: 15px;
  margin: 10px;
}

.category {
  border: 1px solid blue;
  border-radius: 5px;
  box-shadow: 4px white;
  padding: 10px;
  margin: 20px;
}
.category h2 {
  font-family: 'Roboto';
  text-align: center;
  color: red;
  background-color: wheat;
  border-radius: 5px;
}
.category list li {
  list-style: none;
  text-align: center;
  background-color: grey;
}
</style>
