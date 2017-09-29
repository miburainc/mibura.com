import * as TYPE from '../types'
import Vue from 'vue'

import client from '../api/client'

const state = {
	estimate_pdf: null,
	invoice_pdf: null
}

const mutations = {
	[TYPE.SET_ESTIMATE_PDF]: (state, value) => {
		state.estimate_pdf = value
	},
	[TYPE.SET_INVOICE_PDF]: (state, value) => {
		state.invoice_pdf = value
	}
}

const getters = {
	getEstimatePDF: state => state.estimate_pdf,
	getInvoicePDF: state => state.invoice_pdf
}

const actions = {
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
	}
}

export default {
	state,
	mutations,
	getters,
	actions
}