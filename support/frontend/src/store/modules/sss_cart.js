import Vue from 'vue'
import * as TYPE from '../types'

import moment from 'moment'

import freshbooks from '../api/freshbooks'
import cart from '../api/cart'

import {makeid} from '../../scripts/util'
import {PLANS, step_names} from '../values'

const state = {
	cart: [],
	cart_id: -1,
	cart_ref: null,
	plans: PLANS,
	current_plan: 'silver',
	support_months: 12,
	current_item_id: null,
	estimate_id: 0,
	estimate_pdf: null,
	cart_changed: false,
}

const mutations = {
	[TYPE.SET_CURRENT_PLAN]: (state, value) => {
		state.current_plan = value
	},
	[TYPE.CART_ADD_ITEM]: (state, payload) => {
		// NOTE TO SELF: REMOVE LOGIC FROM MUTATION !!!!

		if (payload.rootState.Form.current_item.hasOwnProperty('index')) {
			let index = payload.rootState.Form.current_item.index;
			if (index >= 0) {
				state.cart.splice(index, 1, payload.obj)
			}
		}
		else {
			state.cart.push(payload.obj)
		}
	},
	[TYPE.CART_EDIT_ITEM]: (state, payload) => {
		Vue.set(payload.rootState.Form, 'current_item', state.cart[payload.index])
		Vue.set(payload.rootState.Form.current_item, 'index', payload.index);
	},
	[TYPE.CART_REMOVE_ITEM]: (state, payload) => {
		if (state.cart[payload.index].id !== payload.id) {
			console.error("!!! Error removing cart item")
		}
		else {
			state.cart.splice(payload.index, 1)
		}
	},
	[TYPE.SET_SUPPORT_MONTHS]: (state, payload) => {
		state.support_months = payload
	},
	[TYPE.CART_CLEAR]: (state) => {
		state.cart = []
	},
	[TYPE.CART_SET_ID]: (state, value) => {
		state.cart_id = value
	},
	[TYPE.CART_SET_REF]: (state, value) => {
		state.cart_ref = value
	},
	[TYPE.SET_ESTIMATE_ID]: (state, value) => {
		state.estimate_id = value
	},
	[TYPE.SET_ESTIMATE_PDF]: (state, value) => {
		state.estimate_pdf = value
	},
	[TYPE.CART_CHANGED]: (state, value) => {
		state.cart_changed = value
	}
}

const actions = {
	setCartChanged({commit}, value) {
		commit(TYPE.CART_CHANGED, value)
	},
	addCartItem({commit, dispatch, state, rootState}, payload) {
		let cloud_in_cart_already = false

		if (payload.type == "cloud") {
			for (let i=0; i<state.cart.length; i++) {
				if (state.cart[i].brand == payload.brand) {
					dispatch('addNotification', {
						type: "danger",
						message: "You already have " + payload.brand + " in your cart!<br>Select another provider or click the Skip button."
					})
					cloud_in_cart_already = true
					return false;
				}
			}
		}
		if (!cloud_in_cart_already) {
			dispatch('setCartChanged', true)
			commit(TYPE.CART_ADD_ITEM, {
				rootState: rootState,
				obj: payload
			})
		}
		return true;
	},
	editCartItem({commit, state, rootState}, payload) {
		let global_payload = {
			rootState: rootState,
			index: payload.index,
			id: payload.id
		}
		commit(TYPE.CART_EDIT_ITEM, global_payload)
		commit(TYPE.SET_CURRENT_ITEM, state.cart[payload.index])
		commit(TYPE.SET_CURRENT_FORM_STEP, step_names.additional_info)
	},
	clearCart({commit, dispatch}) {
		dispatch('setCartChanged', true)
		commit(TYPE.CART_CLEAR)
		commit(TYPE.SET_CURRENT_FORM_STEP, 0)
	},
	removeCartItem({commit, dispatch}, payload) {
		dispatch('setCartChanged', true)
		commit(TYPE.CART_REMOVE_ITEM, payload)
	},
	setSupportMonths({commit, dispatch}, payload) {
		let val = payload.target.value
		dispatch('setCartChanged', true)
		commit(TYPE.SET_SUPPORT_MONTHS, val)
	},
	setSupportYears({commit, dispatch}, payload) {
		let val = payload

		if((val > 0) && (val <= 144)){
			dispatch('setCartChanged', true)
			commit(TYPE.SET_SUPPORT_MONTHS, val)
		}
	},
	setCartId({commit}, value) {
		commit(TYPE.CART_SET_ID, value)
	},
	saveCart({state, rootState, commit, dispatch}) {
		let ref = state.cart_ref ? state.cart_ref : makeid(8)
		let client = rootState.Form.client_info
		
		return cart.getOrCreateCart({
				email: client.email,
				client: client.pk,
				reference: ref,
				products: state.cart,
				plan: state.current_plan,
				length: state.support_months/12,
			}).then(response => {
				dispatch('setCartChanged', false)
				commit(TYPE.CART_SET_ID, response.data.pk)
				commit(TYPE.CART_SET_REF, response.data.reference)
			});
	},
	sendQuoteEmail({state}, payload) {
		cart.sendQuoteEmail(state.cart_ref)
		.then((response) => {
			$('#pdfModal').modal('hide')
		})
	},
	setEstimatePdfFile({commit}, payload) {
		commit(TYPE.SET_ESTIMATE_PDF, payload)
	},
	serverGetEstimatePdf({state, rootState, commit}) {
		let client = rootState.Form.client_info
		let cart_ref = state.cart_ref
		return freshbooks.getEstimatePDF(client, cart_ref)
			.then(response => {
				// commit(TYPE.SET_ESTIMATE_ID, response.data.estimate_id)
				var blob=new Blob([response.data], {type:"application/pdf"});
				let file_url = window.URL.createObjectURL(blob)
				commit(TYPE.SET_ESTIMATE_PDF, file_url)
			})
	},
	checkout({commit, dispatch, state, rootState}) {
		let client = rootState.Form.client_info
		if (!state.cart_ref) {
			dispatch('saveCart', client)
		}
		let payment_token = null

		if (rootState.stripe.ach_payment_token != null || rootState.stripe.cc_payment_token != null) {
			payment_token = rootState.stripe.ach_payment_token ? rootState.stripe.ach_payment_token : rootState.stripe.cc_payment_token
		}

		let data = {
			client: client.pk,
			cart: state.cart_ref,
			length: state.support_months/12,
		}
		if (payment_token) {
			data.stripe_token = payment_token
		}

		// Check if unverified items in cart
		let can_checkout = true
		for (let i=0; i<state.cart.length; i++) {
			if (!state.cart[i].verified && state.cart[i].type != "cloud") {
				can_checkout = false;
				console.log("unknown item")
				console.log(state.cart[i])
			}
		}
		if (can_checkout) {
			cart.api_checkout(data)
				.then((response) => {
					dispatch('setPurchaseSuccess', true)
				})
			return true
		}
		else {
			return false // Failed to checkout
		}
	},

	setCurrentPlan({commit, dispatch}, value) {
		dispatch('setCartChanged', true)
		commit(TYPE.SET_CURRENT_PLAN, value)
    },

	
}

const getters = {

	// //////////////
	// Products

	getProductAge: state => product => {
		let product_release = moment(product.release)
		let today = moment()
		let age_months = today.diff(product_release, 'months')
		let age = age_months / 6
		return Math.round(age)
	},
	getProductPrice: (state, store) => cart_index => {
		// 
		// Calculate product price depending on plan selected by customer
		// 
		let cost = 0
		let product = state.cart[cart_index]
		let plan_name = ''
		switch(store.getCurrentPlan) {
			case 'silver':
				// Silver
				plan_name = 'silver'
				break;
			case 'gold':
				// Gold
				plan_name = 'gold'
				break;
			case 'black':
				// Black
				plan_name = 'black'
				break;
		}
		// Product multiplier per plan e.g 1.0x
		let pp = product['price_'+plan_name]
		// Product Category multiplier e.g 1.2x
		let pm = product.category.price_multiplier
		// Plan base product price e.g $49/yr
		let pc = store.getPlan(store.getCurrentPlan).cost

		// Calculation and then divided by half since plans are sold in 6 month increments
		cost = (pp * pm * pc) / 2
		return cost
	},
	getProductSubtotal: (state, store) => cart_index => {
		//
		// Get product line item price
		//
		let product = state.cart[cart_index]
		let product_price = store.getProductPrice(cart_index)

		let product_age = store.getProductAge(product)
		// price_iterations - how many half year increments to add
		let price_iterations = store.getSupportMonths/6
		// inc - amount to add to base price based on product age
		let inc = product.category.yearly_tax
		let price = 0.0
		// Calculate price base price depending on age
		for (let e=0; e<product_age; e++) {
			price += (product_price * inc)
		}

		// Calculate price into future for length of support bought by client
		for (let i=0; i<price_iterations; i++) {
			price += product_price + (product_price * inc)
		}

		return price
	},
	// Total Cart Price
	getTotal: (state, store) => {
		let total = 0;
		for (let i=0; i<state.cart.length; i++) {
			total += store.getProductSubtotal(i)
		}		
		return total
	},
	getGrandTotal: (state, store) => {
		let total = store.getTotal
		let final = total - (total * store.getCurrentDiscount)
		return final
	},
	getCart: state => state.cart,
	getSupportMonths: state => state.support_months,
	getCartReference: state => state.cart_ref,
	getEstimatePDF: state => state.estimate_pdf,
	getEstimateID: state => state.estimate_id,
	getCartChanged: state => state.cart_changed,
	// Plans
	getPlans: state => state.plans,
	getCurrentPlan: state => state.current_plan,
    getPlan: state => plan => {
		// console.log("getPlan", plan)
		// console.log(state.plans.length)
		for (let i=0; i<state.plans.length; i++) {
			if (state.plans[i].code == plan) {
				// console.log("Match found:")
				// console.log(state.plans[i].code, plan)
				return state.plans[i]
			}
		}
		return false
	},
}

export default {
	state,
	getters,
	mutations,
	actions
}