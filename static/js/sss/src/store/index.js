import Vue from 'vue';
import Vuex from 'vuex'

import SSSFormSteps from './modules/sss_formsteps'
import SSSCart from './modules/sss_cart'

import {PLANS, API_ROOT, product_multiplier} from './values'

import productApi from './api/products'

import createLogger from '../scripts/logger'

import * as TYPE from './types'

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production'

export const store = new Vuex.Store({
  state: {
    plans: PLANS,
    current_plan: 'silver',
    api_root: API_ROOT,
    errors: {},
    multiplier: {},
  },
  getters: {
    getMultiplier: state => name => {
      console.log('getMultiplier')
      console.log(state)
      console.log(name)
      for (let i=0; i<state.multiplier.length; i++) {
        let cat = state.multiplier[i]
        if (cat.category_code == name) {
          return cat
        }
      }
    },
    getPlans: state => state.plans,
    getAPIRoot: state => state.api_root,
    getErrors: state => state.errors,
    getCurrentPlan: state => state.current_plan,
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
    },
    [TYPE.SET_CURRENT_PLAN]: (state, value) => {
      state.current_plan = value
    },
    [TYPE.SET_CATEGORY_MULTIPLIER]: (state, payload) => {
      Vue.set(state, 'multiplier', payload)
    }
  },
  actions: {
    setError({commit}, payload) {
      commit('setError', payload)
    },
    clearErrors({commit}) {
      commit('clearErrors')
    },
    setCurrentPlan({commit}, value) {
      console.log("setCurrentPlan")
      
      let val = value.target.value
      let result = ''
      val = parseInt(val)
      switch(val) {
        case 0:
          result = 'silver'
          break;
        case 1:
          result = 'gold'
          break;
        case 2:
          result = 'black'
          break;
      }
      console.log(result)
      commit(TYPE.SET_CURRENT_PLAN, result)
    },
    setCategoryMultipliers({commit}, payload) {
      productApi.getProductCategories((response) => {
        commit(TYPE.SET_CATEGORY_MULTIPLIER, response.data.results)
      })
      
    }
  },
  modules: {
  	SSSFormSteps,
    SSSCart,
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
})