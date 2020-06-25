import Vue from 'vue'
import Vuex from 'vuex'
import constants from '../constants'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    socketio: {
      status: constants.SocketIoStatus.DISCONNECTED
    }
  },
  getters: {
    SocketIoStatus(state) {
      return state.socketio.status
    }
  },
  mutations: {
    SocketIoStatus(state, NewValue) {
      state.socketio.status = NewValue
    }
  },
  actions: {
  },
  modules: {
  }
})
