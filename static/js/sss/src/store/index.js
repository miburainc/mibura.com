import Vue from 'vue';
import Vuex from 'vuex'

import Form from './modules/sss_form'
import Cart from './modules/sss_cart'

import {PLANS, API_ROOT, product_multiplier} from './values'

import freshbooks from './api/freshbooks'
import plaid from './api/plaid'
import productApi from './api/products'

import createLogger from '../scripts/logger'

import * as TYPE from './types'

import moment from 'moment'

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production'

export const store = new Vuex.Store({
  state: {
    plans: PLANS,
    current_plan: 'silver',
    api_root: API_ROOT,
    errors: {},
    multiplier: {},
    brands: [],
    purchase_success: false,
    accepted_terms: false,
    stripe: {},
  },
  getters: {
    getStripe: state => state.stripe,
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
    getBrands: state => state.brands,
    getPlans: state => state.plans,
    getAPIRoot: state => state.api_root,
    getErrors: state => state.errors,
    getCurrentPlan: state => state.current_plan,
    getPurchaseSuccess: state => state.purchase_success,
    getAcceptedTerms: state => state.accepted_terms,
    getPaymentToken: state => {
      if (state.stripe.ach_payment_token) {
        return state.stripe.ach_payment_token
      }
      else if (state.stripe.cc_payment_token) {
        return state.stripe.cc_payment_token
      }
      else {
        return ""
      }
    },
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
    [TYPE.SET_STRIPE_PROP]: (state, payload) => {
      Vue.set(state.stripe, payload.prop, payload.value)
    },
    [TYPE.SET_CURRENT_PLAN]: (state, value) => {
      state.current_plan = value
    },
    [TYPE.SET_CATEGORY_MULTIPLIER]: (state, payload) => {
      Vue.set(state, 'multiplier', payload)
    },
    [TYPE.SET_PRODUCT_BRANDS]: (state, payload) => {
      state.brands = payload
    },
    [TYPE.SET_PURCHASE_SUCCESS]: (state, payload) => {
      state.purchase_success = payload
    },
    [TYPE.SET_ACCEPTED_TERMS]: (state, value) => {
      state.accepted_terms = value
    },
  },
  actions: {
    plaidSendCredentials({commit, state}) {
      plaid.sendPlaidCredentials(state.stripe.ach_account_id, state.stripe.ach_public_token)
        .then((response) => {
          commit(TYPE.SET_STRIPE_PROP, {
            prop: 'ach_payment_token',
            value: response.data
          })
        })
    },
    ServerRequestPastEstimate({commit, state, rootState}, estimate_ref) {
      freshbooks.request_past_estimate(estimate_ref).then((response) => {
        console.log(response)
        commit(TYPE.CART_CLEAR)
        let items = response.data.cart_items
        let cart_obj = {}
        for (let i=0;i<items.length;i++) {
          if (items[i].category.category_code=='cloud') {
          	let cloud = items[i]
          	let category = null
						for (let e=0; e<state.multiplier.length; e++) {
							let cat = state.multiplier[e]
							console.log(cat)
							if (cat.category_code == cloud.category.category_code) {
								category = cat
							}
						}

            cart_obj = {
							sku: 'none',
							category: category,
							price_silver: cloud.price_multiplier,
              price_gold: cloud.price_multiplier,
              price_black: cloud.price_multiplier,
              price_multiplier: cloud.price_multiplier,
              type: 'cloud',
              brand: cloud.name,
              model: '',
              release: moment().format("YYYY-MM-DD"),
            }
          }
          else {
          	cart_obj = {
          		...items[i]
          	}
          }

          // Now commit the object to the cart
          commit(TYPE.CART_ADD_ITEM, {obj:cart_obj, rootState:rootState})
        }
        commit(TYPE.CLEAR_CLIENT)
        commit(TYPE.SET_CLIENT, response.data.client)
        commit(TYPE.SET_CURRENT_PLAN, response.data.cart.plan)
      	commit(TYPE.SET_SUPPORT_MONTHS, response.data.cart.length*12)
        $('#estimateIdModal').modal('hide')
      })
    },
    setStripeProp({commit}, payload) {
      commit(TYPE.SET_STRIPE_PROP, payload)
    },
    setAcceptedTerms({commit}, value) {
      commit(TYPE.SET_ACCEPTED_TERMS, value)
    },
    setError({commit}, payload) {
      commit('setError', payload)
    },
    clearErrors({commit}) {
      commit('clearErrors')
    },
    setCurrentPlan({commit}, value) {
      console.log("setCurrentPlan")
      
      commit(TYPE.SET_CURRENT_PLAN, value)
    },
    setCategoryMultipliers({commit}, payload) {
      productApi.getProductCategories((response) => {
        commit(TYPE.SET_CATEGORY_MULTIPLIER, response.data.results)
      }) 
    },
    setProductBrands({commit}, payload) {
      productApi.getProductBrands((response) => {
        commit(TYPE.SET_PRODUCT_BRANDS, response.data.results)
      }) 
    },
    setPurchaseSuccess({commit}, payload) {
      commit(TYPE.SET_PURCHASE_SUCCESS, payload)
    }
  },
  modules: {
  	Form,
    Cart,
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
})