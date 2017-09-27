import Vue from 'vue'

import * as TYPE from './types'

export default {
	setError (state, payload) {
		Vue.set(state.errors, payload.key, payload.value)
	},
	clearErrors (state) {
		Vue.set(state, 'errors', {})
	},
	clearError(state, name) {
		Vue.set(state.errors, name, null)
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

	// PDFS
	[TYPE.SET_ESTIMATE_PDF]: (state, value) => {
		state.estimate_pdf = value
	},
	[TYPE.SET_INVOICE_PDF]: (state, value) => {
		state.invoice_pdf = value
	},
}