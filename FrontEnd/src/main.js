import {createApp} from 'vue'
import App from './App.vue'
import router from './router' // Import the router configuration

const app = createApp(App)

app.use(router)

app.mount('#app')

//starting point of the frontend main.js the next is the router.js
//creating app from the vue 
//using router and wrapping with the app
