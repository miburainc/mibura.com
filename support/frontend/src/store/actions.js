import freshbooks from './api/freshbooks'
import plaid from './api/plaid'
import stripe from './api/stripe'
import productApi from './api/products'
import cart from './api/cart'
import paymentApi from './api/payment'

import {step_names} from './values'

import * as TYPE from './types'

export default {

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

	
}