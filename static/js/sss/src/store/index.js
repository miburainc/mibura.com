import Vue from 'vue';
import Vuex from 'vuex'

import SSSFormSteps from './modules/sss_formsteps'
import SSSCart from './modules/sss_cart'

import {PLANS, API_ROOT} from './values'

import createLogger from '../scripts/logger'

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production'

export const store = new Vuex.Store({
  state: {
    plans: PLANS,
    api_root: API_ROOT,
    errors: {},
  },
  getters: {
    getPlans: state => state.plans,
    getAPIRoot: state => state.api_root,
    getErrors: state => state.errors
  },
  mutations: {
    increment (state) {
      state.count++
    },
    setError (state, payload) {
      Vue.set(state.errors, payload.key, payload.value)
    },
    clearErrors (state) {
      Vue.set(state, 'errors', {})
    }
  },
  actions: {
    setError({commit}, payload) {
      commit('setError', payload)
    },
    clearErrors({commit}) {
      commit('clearErrors')
    }
  },
  modules: {
  	SSSFormSteps,
    SSSCart,
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
})