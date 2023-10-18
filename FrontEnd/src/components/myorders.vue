<template>
  <div>
    <userNavbar />
    <div class="container-xxl flex-grow-1 container-p-y mt-5">
      <div class="row d-flex justify-content-center">
        <div class="col-lg-6">
          <h3>Welcome {{ username }}</h3>
          <div class="card">
            <div v-if="no_order">
              <h3>No orders in your cart. Try adding some products.</h3>
              <a
                href="/userHome"
                class="text-white btn btn-primary m-3 text-decoration-none"
                >Add to Cart</a
              >
            </div>
            <div v-else class="card-body">
              <h4>Recent Products Added to the Order Section</h4>
              <div class="d-flex flex-row justify-content-between">
                <div>Product</div>
                <div>Price</div>
                <div>Quantity</div>
                <div>Amount</div>
              </div>
              <ul class="list-group">
                <li
                  v-for="(category_product, index) in orders"
                  :key="index"
                  class="list-group-item"
                >
                  <div class="d-flex justify-content-between">
                    <div>{{ category_product.product_name }}</div>
                    <div>
                      <p class="text-warning">
                        {{ category_product.price }} /-
                        {{ category_product.units }}
                      </p>
                    </div>
                    <div>
                      <p class="text-success">
                        {{ category_product.Quantity }}
                        {{ category_product.units }}
                      </p>
                    </div>
                    <div>
                      <p class="text-success">
                        {{ category_product.amount }}
                      </p>
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
import Cookies from 'js-cookie'
import axios from 'axios'
import userNavbar from './custom/userNavbar'

export default {
  name: 'user-orders',
  components: {
    userNavbar,
  },
  data() {
    return {
      username: Cookies.get('username'),
      orders: [],
      no_order: false,
    }
  },
  mounted() {
    this.getOrders()
  },
  methods: {
    async getOrders() {
      const user_id = Cookies.get('logged_id')
      const data = {
        user_id: user_id,
      }
      try {
        const response = await axios.post(
          'http://localhost:5050/orderTable',
          data,
        )
        console.log(response)
        if (response.data.length !== 0) {
          this.orders = response.data.orders_list
          console.log(this.orders)
        } else {
          this.no_order = true
        }
      } catch (error) {
        console.log(error)
      }
    },
  },
}
</script>
