import freshbooks from './api/freshbooks'
import plaid from './api/plaid'
import stripe from './api/stripe'
import productApi from './api/products'
import cart from './api/cart'

import {step_names} from './values'

import * as TYPE from './types'

export default {
  plaidSendCredentials({commit, state}) {
    plaid.sendPlaidCredentials(state.stripe.ach_account_id, state.stripe.ach_public_token)
      .then((response) => {
        commit(TYPE.SET_STRIPE_PROP, {
          prop: 'ach_payment_token',
          value: response.data
        })
      })
  },
  achSendCredentials({commit, rootState}, achToken) {
    stripe.postAchCredentials(rootState.Form.client_info.pk, achToken)
      .then((response) => {
        console.log(response)
        commit(TYPE.SET_PAYMENT_PROP, {prop: 'checkouttype', data: 'achsubmitted'})
        
        commit(TYPE.SET_CURRENT_FORM_STEP, step_names.success)
      })
  },
  achSendVerify({commit, rootState}) {
    stripe.postAchVerify(rootState.Form.client_info.pk, rootState.Form.payment_info.verify1, rootState.Form.payment_info.verify2)
      .then((response) => {
        if (response.response) {
          // Error
          commit(TYPE.ADD_NOTIFICATION, {type: 'danger',message: response.response.data})
        }
        else if (response.status == 200) {
          commit(TYPE.SET_PAYMENT_PROP, {prop: 'checkouttype', data: 'ach'})
          commit(TYPE.SET_PAYMENT_PROP, {prop: 'payment_token', data: 'ach'})
          commit(TYPE.ADD_NOTIFICATION, {type: 'success',message: "Successfully verified bank account.  Please proceed to checkout"})
          
          commit(TYPE.SET_CURRENT_FORM_STEP, step_names.verify)
        }
        
        // commit(TYPE.SET_STRIPE_PROP, {
        //   prop: 'ach_payment_token',
        //   value: response.data
        // })
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
  clearError({commit}, name) {
    commit('clearError', name)
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
  },

  // PDFS

  serverGetInvoicePdf({state, rootState, commit}) {
    let client = rootState.Form.client_info
    let cart_ref = state.cart_ref
    return freshbooks.getInvoicePDF(client, cart_ref)
      .then(response => {
        // commit(TYPE.SET_ESTIMATE_ID, response.data.estimate_id)
        var blob=new Blob([response.data], {type:"application/pdf"});
        let file_url = window.URL.createObjectURL(blob)
        commit(TYPE.SET_INVOICE_PDF, file_url)
      })
  },

  setEstimatePdfFile({commit}, payload) {
    commit(TYPE.SET_ESTIMATE_PDF, payload)
  },
  setInvoicePdfFile({commit}, payload) {
    commit(TYPE.SET_INVOICE_PDF, payload)
  },
}