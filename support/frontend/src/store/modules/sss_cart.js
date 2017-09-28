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
	
	cart_changed: true,
}

const mutations = {
	[TYPE.SET_CART]: (state, array) =>{
		state.cart = array
	},
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
	
	[TYPE.CART_CHANGED]: (state, value) => {
		state.cart_changed = value
	},
	[TYPE.SET_CART_STATUS]: (state, value) => {
		state.cart_status = value
	},
}

const actions = {
	setCartStatus({commit}, value){
		commit(TYPE.SET_CART_STATUS, value)
	},
	setCart({commit}, payload){
		commit(TYPE.SET_CART, payload.items)
		commit(TYPE.CART_SET_ID, payload.id)
		commit(TYPE.CART_SET_REF, payload.reference)
		commit(TYPE.SET_CURRENT_PLAN, payload.plan)
	},
	setCartChanged({commit}, value) {
		commit(TYPE.CART_CHANGED, value)
	},
	checkDuplicateCloud({commit, state, dispatch, rootState}, value){
		console.log("asdffdsasadf")
		for (let i=0; i<state.cart.length; i++) {
			if (state.cart[i].brand == value) {
				dispatch('addNotification', {
					type: "danger",
					message: "You already have " + value + " in your cart!<br>Select another provider or click the Skip button."
				})
				commit(TYPE.SET_CLOUD_IN_CART_ALREADY, true)
				return
			}
		}
		commit(TYPE.SET_CLOUD_IN_CART_ALREADY, false)
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
				cart_status: state.cart_status,
			}).then(response => {
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
					console.log(response)
					var blob=new Blob([response.data], {type:"application/pdf"});
					let file_url = window.URL.createObjectURL(blob)
					dispatch('setInvoicePdfFile', file_url)
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
		console.log(product)
		let pp = product['price_'+plan_name]
		
		// Product Category multiplier e.g 1.2x
		let pm = product.category.price_multiplier
		
		let pa = 0
		let pt = 0

		let pq = 0
		let qm = 0

		if(product.quantity != null){
			pq = product.quantity
			qm = product.quantity_multiplier
		}
		else{
			if(product.type == "product"){
				let product_release = moment(product.age)
				let today = moment()
				let age_months = today.diff(product_release, 'months')
				let final_age = age_months / 6
				pa = final_age
			}
			else{
				pa = product.age
			}
			
			pt = product.category.yearly_tax
		}

		// Plan base product price e.g $49/yr
		let pc = store.getPlan(store.getCurrentPlan).cost
		// Calculation and then divided by half since plans are sold in 6 month increments
		cost = (pc * pp * (pm + pq * qm + pa * pt)) / 2

		console.log("ASDDFASDASFAFASD")
		console.log(pp)
		console.log(pc)
		console.log(pm)
		console.log(pq)
		console.log(pa)
		console.log(qm)
		console.log(pt)

		return cost
	},
	getProductSubtotal: (state, store) => cart_index => {
		let product_price = store.getProductPrice(cart_index)
		// price_iterations - how many half year increments to add
		let price_iterations = store.getSupportMonths/6
		
		let price = product_price * price_iterations

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
	getCloudInCartAlready: state => state.cloud_in_cart_already,
	getCart: state => state.cart,
	getCartId: state => state.cart_id,
	getSupportMonths: state => state.support_months,
	getCartReference: state => state.cart_ref,
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
	getUnverifiedItems: state => {
		let items = []

		for (let i=0; i<state.cart.length; i++){
			if(state.cart[i].type == "unknown"){
				items.push(state.cart[i])
			}
		}
		return items
	},
}

export default {
	state,
	getters,
	mutations,
	actions
}