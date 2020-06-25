import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import socketio from 'socket.io-client'
import constants from './constants'

Vue.config.productionTip = false

const io = socketio('http://192.168.1.243:8088')

io.on('connect',()=> {
  console.log('Connected')
  store.commit('SocketIoStatus', constants.SocketIoStatus.CONNECTED)
})

io.on('disconnect',()=> {
  console.log('Disconnected')
  store.commit('SocketIoStatus', constants.SocketIoStatus.DISCONNECTED)
})

new Vue({
  router,
  io,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
