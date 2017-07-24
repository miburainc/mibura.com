import * as TYPE from '../types'

const state = {
	cart: [],
}

const mutations = {
	[TYPE.CART_ADD_ITEM]: (state, payload) => {
		state.cart.push(payload)
	},
	[TYPE.CART_REMOVE_ITEM]: (state, payload) => {
		if (state.cart[payload.index].id !== payload.id) {
			console.error("!!! Error removing cart item")
		}
		else {
			state.cart.splice(payload.index, 1)
		}
	}
}

const actions = {
	addCartItem({commit}, payload) {
		commit(TYPE.CART_ADD_ITEM, payload)
	},
	removeCartItem({commit}, payload) {
		commit(TYPE.CART_REMOVE_ITEM, payload)
	}
}

const getters = {
	getCart: state => state.cart,
}

export default {
	state,
	getters,
	mutations,
	actions
}