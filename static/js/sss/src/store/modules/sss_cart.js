import Vue from 'vue'
import * as TYPE from '../types'
import {step_names} from '../values'
const state = {
	cart: [],
	support_months: 12,
	current_item_id: null,
}

const mutations = {
	[TYPE.CART_ADD_ITEM]: (state, payload) => {
		console.log("CART_ADD_ITEM")
		if (payload.rootState.SSSFormSteps.current_item.hasOwnProperty('index')) {
			console.log("Index found, editing")
			let index = payload.rootState.SSSFormSteps.current_item.index;
			console.log("Index: ", index)

			
			if (index >= 0) {
				console.log("payload.rootState.SSSFormSteps.products")
				console.log(payload.rootState.SSSFormSteps.products[payload.obj.model])
				state.cart.splice(index, 1, payload.obj)
			}
		}
		else {
			console.log("Index not found, adding")
			state.cart.push(payload.obj)
		}
	},
	[TYPE.CART_EDIT_ITEM]: (state, payload) => {
		Vue.set(payload.rootState.SSSFormSteps, 'current_item', state.cart[payload.index])
		
		Vue.set(payload.rootState.SSSFormSteps.current_item, 'index', payload.index);
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
	}
}

const getters = {
	getCart: state => state.cart,
	getSupportMonths: state => state.support_months,
}

export default {
	state,
	getters,
	mutations,
	actions
}