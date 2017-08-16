import Vue from 'vue'
import * as TYPE from '../types'

import freshbooks from '../api/freshbooks'
import cart from '../api/cart'

import {makeid} from '../../scripts/util'
import {step_names} from '../values'

const state = {
	cart: [],
	cart_id: -1,
	cart_ref: '',
	support_months: 12,
	current_item_id: null,
	estimate_id: 0,
	estimate_pdf: null,
}

const mutations = {
	[TYPE.CART_ADD_ITEM]: (state, payload) => {
		console.log("CART_ADD_ITEM")
		if (payload.rootState.Form.current_item.hasOwnProperty('index')) {
			console.log("Index found, editing")
			let index = payload.rootState.Form.current_item.index;
			console.log("Index: ", index)

			
			if (index >= 0) {
				console.log("payload.rootState.Form.products")
				console.log(payload.rootState.Form.products[payload.obj.model])
				state.cart.splice(index, 1, payload.obj)
			}
		}
		else {
			console.log("Index not found, adding")
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
	}
}

const actions = {
	addCartItem({commit, rootState}, payload) {
		commit(TYPE.CART_ADD_ITEM, {
			rootState: rootState,
			obj: payload
		})
	},
	editCartItem({commit, state, rootState}, payload) {
		console.log("Edit: " + payload.id)
		let global_payload = {
			rootState: rootState,
			index: payload.index,
			id: payload.id
		}
		commit(TYPE.CART_EDIT_ITEM, global_payload)
		commit(TYPE.SET_CURRENT_ITEM, state.cart[payload.index])
		commit(TYPE.SET_CURRENT_FORM_STEP, step_names.additional_info)
	},
	clearCart({commit}) {
		commit(TYPE.CART_CLEAR)
	},
	removeCartItem({commit}, payload) {
		commit(TYPE.CART_REMOVE_ITEM, payload)
	},
	setSupportMonths({commit}, payload) {
		let val = payload.target.value

		commit(TYPE.SET_SUPPORT_MONTHS, val)
	},
	setSupportYears({commit}, payload) {
		let val = payload.target.value
		
		commit(TYPE.SET_SUPPORT_MONTHS, val*12)
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
				plan: rootState.current_plan,
				length: state.support_months/12,
			}).then(response => {
				commit(TYPE.CART_SET_ID, response.data.pk)
				commit(TYPE.CART_SET_REF, response.data.reference)
			});
	},
	setEstimatePdfFile({commit}, payload) {
		commit(TYPE.SET_ESTIMATE_PDF, payload)
	},
	serverGetEstimatePdf({state, rootState, commit}) {
		let client = rootState.Form.client_info
		let cart_ref = state.cart_ref
		console.log("serverGetEstimatePdf")
		console.log("client", client)
		console.log("cart_ref", cart_ref)
		return freshbooks.getEstimatePDF(client, cart_ref)
			.then(response => {
				console.log("serverGetEstimatePdf__response")
				console.log(response)
				// commit(TYPE.SET_ESTIMATE_ID, response.data.estimate_id)
				var blob=new Blob([response.data], {type:"application/pdf"});
				let file_url = window.URL.createObjectURL(blob)
				commit(TYPE.SET_ESTIMATE_PDF, file_url)
			})
	},
	checkout({state, rootState, commit, dispatch}) {
		let client = rootState.Form.client_info
		if (!state.cart_ref) {
			dispatch('saveCart', client)
		}
		let data = {
			client: client.pk,
			cart: state.cart_ref,
			length: state.support_months/12,
			stripe_token: rootState.Form.payment_token
		}
		console.log(client)
		console.log(state.cart_ref)
		cart.checkout(
			data,
			(response) => {
				console.log(response)
				dispatch('setPurchaseSuccess', true)
			});
	}
}

const getters = {
	getCart: state => state.cart,
	getSupportMonths: state => state.support_months,
	getCartReference: state => state.cart_ref,
	getEstimatePDF: state => state.estimate_pdf,
	getEstimateID: state => state.estimate_id,
}

export default {
	state,
	getters,
	mutations,
	actions
}