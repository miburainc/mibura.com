import * as TYPE from '../types'
import Vue from 'vue'

import client from '../api/client'
import payment_api from '../api/payment'

import {form_steps} from '../values'

const state = {
	payment_info: {},
	payment_object: {},
	payment_token: "",
	payment_processing: false,
}

const mutations = {
	[TYPE.SET_PAYMENT_PROCESSING]: (state, value) => {
		state.payment_processing = value
	},
	[TYPE.SET_PAYMENT_PROP]: (state, payload) => {
		Vue.set(state.payment_info, payload.prop, payload.data)
	},
	[TYPE.SET_PAYMENT_TOKEN]: (state, value) => {
		state.payment_token = value
	},
	[TYPE.SET_PAYMENT_OBJECT]: (state, payload) => {
		Vue.set(state.payment_object, payload.prop, payload.data)
	}
}

const actions = {
	createPaymentObject({commit}, payload) {
		payment_api.serverCreatePayment(payload)
			.then(response => {
				console.log(response)
				for (let key in response.data) {
					if (response.data.hasOwnProperty(key)) {
						let payload = {
							prop: key,
							data: response.data[key]
						}
						commit(TYPE.SET_PAYMENT_OBJECT, payload)
					}
				}
				
			})
	},
	plaidSendCredentials({commit, state}) {
		plaid.sendPlaidCredentials(state.stripe.ach_account_id, state.stripe.ach_public_token)
			.then((response) => {
				commit(TYPE.SET_PAYMENT_PROP, {
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
		.then(
			response => {

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
			}
		)
	},
	sendPaymentPoNumber({commit, getters, state, rootState}, payload) {
		console.log("sendPaymentPoNumber begin")
		console.log(payload)
		
		payment_api.sendPaymentPoNumber(payload)
			.then((response) => {
				commit(TYPE.SET_PURCHASE_SUCCESS, true)
				console.log("sendPaymentPoNumber response")
				console.log(response)
			})
	},
	setPaymentProcessing({commit}, value){
		commit(TYPE.SET_PAYMENT_PROCESSING, value)
	},
	setPaymentProp({commit}, payload) {
		commit(TYPE.SET_PAYMENT_PROP, payload)
	},
	setPaymentToken({commit}, value) {
		commit(TYPE.SET_PAYMENT_TOKEN, value)
	}
}

const getters = {
	getPaymentProcessing: state => state.payment_processing,
	getPaymentInfo: state => state.payment_info,
	getPaymentInfoProp: state => prop => state.payment_info[prop],
	getAchPaymentToken: state => {
		if (state.payment_info.ach_payment_token) {
			return state.payment_info.ach_payment_token
		}
		else {
			return ""
		}
	},
	getPaymentToken: state => {
		if (state.payment_info.ach_payment_token) {
			return state.payment_info.ach_payment_token
		}
		else if (state.payment_info.cc_payment_token) {
			return state.payment_info.cc_payment_token
		}
		else {
			return ""
		}
	},
}

export default {
	state,
	getters,
	mutations,
	actions
}