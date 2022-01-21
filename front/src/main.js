// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueNativeSock from 'vue-native-websocket'
import VueAxios from 'vue-axios'
import axios from 'axios'

Vue.use(VueNativeSock, `ws://${window.location.host}/ws/`, {
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 500
})
Vue.use(VueAxios, axios)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  components: { App },
  template: '<App/>'
})
