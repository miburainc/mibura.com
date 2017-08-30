import Vue from 'vue';
import Vuex from 'vuex'

import Form from './modules/sss_form'
import Cart from './modules/sss_cart'

import {API_ROOT, product_multiplier} from './values'

import freshbooks from './api/freshbooks'
import plaid from './api/plaid'
import productApi from './api/products'
import cart from './api/cart'

import createLogger from '../scripts/logger'

import * as TYPE from './types'

import moment from 'moment'

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production'

export const store = new Vuex.Store({
  state: {
    api_root: API_ROOT,
    errors: {},
    multiplier: {},
    brands: [],
    purchase_success: false,
    accepted_terms: false,
    stripe: {},
    discounts: [],
    current_discount: 0.0,
  },
  getters: {
    getStripe: state => state.stripe,
    getMultiplier: state => name => {
      for (let i=0; i<state.multiplier.length; i++) {
        let cat = state.multiplier[i]
        if (cat.category_code == name) {
          return cat
        }
      }
    },
    getBrands: state => state.brands,
    getDiscounts: state => state.discounts,
    getCurrentDiscount: (state, store) => {
      let years = store.getSupportMonths/12
      let discount = 0.0
      
      for (let i=0; i<state.discounts.length; i++) {
        if (state.discounts[i].year_threshold <= years) {
          if (discount < state.discounts[i].discount_percent) {
            discount = state.discounts[i].discount_percent
          }
        }
      }
      return discount
    },
    getAPIRoot: state => state.api_root,
    getErrors: state => state.errors,
    
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
    setError (state, payload) {
      Vue.set(state.errors, payload.key, payload.value)
    },
    clearErrors (state) {
      Vue.set(state, 'errors', {})
    },
    [TYPE.SET_STRIPE_PROP]: (state, payload) => {
      Vue.set(state.stripe, payload.prop, payload.value)
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
    [TYPE.SET_DISCOUNTS]: (state, discounts) => {
      state.discounts = discounts
    },
    [TYPE.SET_CURRENT_DISCOUNT]: (state, value) => {
      state.current_discount = value
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
        commit(TYPE.CART_CLEAR)
        let items = response.data.cart_items
        let cart_obj = {}
        for (let i=0;i<items.length;i++) {
          if (items[i].category.category_code=='cloud') {
          	let cloud = items[i]
          	let category = null
						for (let e=0; e<state.multiplier.length; e++) {
							let cat = state.multiplier[e]
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

    setDiscounts({commit}) {
      cart.serverGetDiscounts()
        .then((response) => {
          commit(TYPE.SET_DISCOUNTS, response.data.results)
        })
    },
    setCurrentDiscount({commit}, value) {
      commit(TYPE.SET_CURRENT_DISCOUNT, value)
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