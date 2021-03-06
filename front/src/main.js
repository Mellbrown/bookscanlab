import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import windowEvent from '@/comp/small/windowEvent'

import '@/util.scss'

library.add(fas)
Vue.component('icon', FontAwesomeIcon)
Vue.component('window-event', windowEvent)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
