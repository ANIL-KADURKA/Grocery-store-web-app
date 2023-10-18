<template>
  <div>
    <div>
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
          <a class="navbar-brand nav-element" href="/userHome">Grocery Store</a>
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="/myCart">My Cart</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/orders">My Orders</a>
            </li>
          </ul>
          <form class="form-inline my-2 my-lg-0 d-flex flex-row">
            <input
              class="form-control mr-2"
              type="search"
              placeholder="Search with Product or price "
              aria-label="Search"
              v-model="searchProduct"
              @input="onChangeSearchInputProduct"
            />
          </form>

          <ul class="navbar-nav ml-auto">
            <li>
              <button
                class="btn btn-outline-danger my-2 my-sm-0"
                @click="logout"
              >
                Logout
              </button>
            </li>
          </ul>
        </div>
      </nav>
    </div>
    <div class="container-xxl flex-grow-1 container-p-y mt-5">
      <div class="row d-flex justify-content-center">
        <h1 class="text-center">Welcome {{ username }}</h1>
        <div class="form-group col-lg-3">
          <label for="categories">Choose Category:</label>
          <select
            class="form-control"
            v-model="selectCategory"
            @change="getFilteredProducts"
            id="categories"
          >
            <option value="0">All Categories</option>
            <option
              v-for="(category, index) in categories"
              :value="category.category_id"
              :key="index"
            >
              {{ category.category_name }}
            </option>
          </select>
        </div>

        <div class="col-lg-6">
          <div class="card">
            <div class="card-body" v-if="no_products">
              <h1>No Products on your Filter</h1>
            </div>
            <div v-else class="card-body">
              <h4 v-if="flash_message" class="text-success">
                {{ flash_message }}
              </h4>
              <h4>All Products Available</h4>
              <div class="d-flex flex-row justify-content-between">
                <div class="mr-4">Category Name</div>
                <div class="mr-4">Product Name</div>
                <div>Price</div>
                <div class="mr-3">No of Items</div>
                <div class="mr-3">Add to Cart</div>
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
                          {{ category_product.Quantity }} Items
                        </p>
                      </div>
                      <div v-else>
                        <p class="text-danger">Out of Stock</p>
                      </div>
                    </div>
                    <button
                      v-if="!isProductInCart(category_product.product_name)"
                      @click="addingToCart(category_product.product_name)"
                      class="btn btn-primary btn-block"
                    >
                      Add to Cart
                    </button>
                    <button v-else class="btn btn-warning btn-block" disabled>
                      Added
                    </button>
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
import Cookies from 'js-cookie'
import axios from 'axios'

export default {
  name: 'user-Home',
  data() {
    return {
      category_products: [],
      username: Cookies.get('username'),
      categories: [],
      selectCategory: 0,
      searchProduct: '',
      no_products: false,
      addedProducts: [],
      flash_message: '',
    }
  },
  mounted() {
    this.getFilteredProducts()
    this.fetchCategories()
    this.getCartProducts()
  },
  methods: {
    logout() {
      Cookies.remove('logged_id')
      Cookies.remove('jwt_token')
      Cookies.remove('username')
      Cookies.remove('role')
      this.$router.push('/')
    },
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
    isProductInCart(productName) {
      if (this.addedProducts) {
        return this.addedProducts.some(
          item => item.product_name === productName,
        )
      }
    },
    async getFilteredProducts() {
      //api call for filtering products with categories based on drop down category value and storing in the categories list
      const data = {
        category: this.selectCategory,
      }
      console.log(this.selectCategory)
      try {
        const response = await axios.post(
          'http://localhost:5050/filterProducts',
          data,
        )
        console.log(response)
        this.category_products = response.data.category_products
        console.log(this.category_products)
      } catch (error) {
        console.log(error)
      }
    },
    async addingToCart(product_name) {
      //api call for adding to cart based on the user-id and product name
      const user_id = Cookies.get('logged_id')
      const data = {
        user_id: user_id,
        product_name: product_name,
      }
      await axios
        .post('http://localhost:5050/add_to_cart', data)
        .then(response => {
          console.log(response.data.message)
          this.flash_message = response.data.message
          this.getFilteredProducts()
        })
        .catch(error => {
          console.error(error)
        })
    },
    async getCartProducts() {
      //api call for fetching cartProducts and storing in the cart list
      const user_id = Cookies.get('logged_id')
      console.log(user_id)
      await axios
      try {
        const response = await axios.post('http://localhost:5050/getcart', {
          user_id: user_id,
        })
        console.log(response)
        if (response.status !== 202) {
          this.addedProducts = response.data.cartList
          console.log(this.addedProducts)
        }
      } catch (error) {
        console.log(error)
      }
    },
    onChangeSearchInputProduct() {
      //filtering and checking rendering the data in the category_products list based on the search input which applies filter for price and the name
      console.log(this.searchProduct)
      const searchInput = this.searchProduct.toLowerCase()
      if (searchInput != '') {
        const new_category_products = this.category_products.filter(
          category_product => {
            const productName = category_product.product_name.toLowerCase()
            const rate = category_product.price.toString().toLowerCase()
            return (
              productName.includes(searchInput) || rate.includes(searchInput)
            )
          },
        )
        this.category_products = new_category_products
        if (this.category_products.length == 0) {
          this.no_products = true
        }
      } else {
        console.log('HelloWorld')
        this.getFilteredProducts()
      }
    },
  },
}
</script>
