<template>
  <div>
    <userNavbar />
    <div class="container-xxl flex-grow-1 container-p-y mt-5">
      <div class="row d-flex justify-content-center">
        <div class="col-lg-6">
          <h3>Welcome {{ username }}</h3>
          <div class="card">
            <div v-if="no_cart">
              <h3>No produts in your cart Try to add</h3>
              <a
                href="/userHome"
                class="text-white btn btn-primary m-3text-decoration-none"
                >Add to Cart</a
              >
            </div>
            <div v-else class="card-body">
              <h4>Recent Products Added to Cart Section</h4>
              <div class="d-flex flex-row justify-content-between">
                <div>Category</div>
                <div>Product</div>
                <div>Price</div>
                <div>Available</div>
                <div>Quantity</div>
                <div>Delete</div>
              </div>
              <ul class="list-group">
                <li
                  v-for="(category_product, index) in cart"
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
                    <div>
                      <input
                        id="category_product.product_id"
                        type="number"
                        v-model="quantity[category_product.product_id]"
                        class="form-control"
                        style="height: 30px; width: 100px"
                        :min="1"
                        :max="category_product.Quantity"
                        @blur="updateItemAmount(category_product)"
                      />
                      <div
                        v-if="
                          quantity[category_product.product_id] < 1 ||
                          quantity[category_product.product_id] >
                            category_product.Quantity
                        "
                        class="invalid-feedback"
                      >
                        Quantity must be between 1 and
                        {{ category_product.Quantity }}
                      </div>
                    </div>
                    <div>
                      <button
                        @click="deletingFromCart(category_product.product_name)"
                        class="btn btn-danger btn-block"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                </li>
              </ul>
            </div>

            <div v-if="cartAmount !== 0">
              <button class="btn btn-primary m-5">
                Total Cart Products Price: {{ cartAmount }}
              </button>
            </div>
            <div v-if="flash_message">
              <h4 class="text-success m-3">
                {{ flash_message }}
              </h4>
            </div>
            <div>
              <button @click="orderNow" class="btn btn-primary m-5">
                Order Now
              </button>
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
import userNavbar from './custom/userNavbar'
export default {
  name: 'user-cart',
  components: {
    userNavbar,
  },
  data() {
    return {
      username: Cookies.get('username'),
      cart: [],
      no_cart: false,
      quantity: {},
      IndividualAmount: {},
      cartAmount: 0,
      flash_message: '',
    }
  },
  mounted() {
    this.getCartProducts()
    this.getFinalCartAmount()
  },
  methods: {
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
          this.cart = response.data.cartList
          console.log(this.cart)
        } else {
          this.no_cart = true
        }
        console.log(this.cart)
      } catch (error) {
        console.log(error)
      }
    },
    updateItemAmount(category_product) {
      const quanta = this.quantity[category_product.product_id]
      const maxQuanta = category_product.Quantity

      if (quanta < 1) {
        this.quantity[category_product.product_id] = 1
      } else if (quanta > maxQuanta) {
        this.quantity[category_product.product_id] = maxQuanta
      }
      this.IndividualAmount[category_product.product_id] =
        category_product.price * this.quantity[category_product.product_id]
      console.log(this.quantity)
      console.log(this.IndividualAmount)
      this.getFinalCartAmount()
    },
    getFinalCartAmount() {
      console.log('Hello World')

      const sum = Object.values(this.IndividualAmount).reduce(
        (sum1, val1) => sum1 + val1,
        0,
      )
      console.log(sum)
      this.cartAmount = sum
    },
    async orderNow() {
      const user_id = Cookies.get('logged_id')
      console.log(user_id)
      await axios
      try {
        const response = await axios.post('http://localhost:5050/orders', {
          user_id: user_id,
          quantity: this.quantity,
          amount: this.IndividualAmount,
        })
        console.log(response)
        this.flash_message = response.data.message
      } catch (error) {
        console.log(error)
      }
    },
    async deletingFromCart(product_name) {
      //api call for deleting from cart based on the user-id and product name
      const user_id = Cookies.get('logged_id')
      const data = {
        user_id: user_id,
        product_name: product_name,
      }
      await axios
        .post('http://localhost:5050/remove_from_cart', data)
        .then(response => {
          console.log(response.data.message)
          this.flash_message = response.data.message
          this.getFilteredProducts()
        })
        .catch(error => {
          console.error(error)
        })
    },
  },
}
</script>
