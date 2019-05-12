import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    rHost: 'http://localhost:80',
    source: [],
    selectedSource: 'a.png'
  },
  mutations: {
    setServer (state, host) {
      state.rHost = host
    },
    setSource (state, list) {
      state.source = list
    },
    selectSource (state, source) {
      state.selectedSource = source
    }
  },
  getters: {

  },
  actions: {
    syncListSource ({ state, commit }) {
      return axios.get(`${state.rHost}/list-source`).then(body => {
        commit('setSource', body.data)
      })
    }
  }
})
