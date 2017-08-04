import * as TYPE from '../types'
import Vue from 'vue'

import client from '../api/client'

import {form_steps} from '../values'

const state = {
	steps: form_steps,
	products: {},
	current_item: {},
	current_form_step: 0,
	client_info: {},
	payment_token: "",
}

const mutations = {
	[TYPE.ADD_PRODUCT]: (state, payload) => {
		state.products[payload.id] = payload.data
	},
	[TYPE.SET_CURRENT_ITEM]: (state, payload) => {
		Vue.set(state, 'current_item', payload)
	},
	[TYPE.SET_CURRENT_ITEM_PROP]: (state, payload) => {
		Vue.set(state.current_item, payload.prop, payload.data)
	},
	[TYPE.SET_CLIENT_PROP]: (state, payload) => {
		Vue.set(state.client_info, payload.prop, payload.data)
	},
	[TYPE.SET_CURRENT_FORM_STEP]: (state, value) => {
		state.current_form_step = value
	},
	[TYPE.CLEAR_CURRENT_FORM_STEP]: (state) => {
		state.current_item = {}
	},
	[TYPE.SET_PAYMENT_TOKEN]: (state, value) => {
		state.payment_token = value
	},
}

const actions = {
	addProduct({commit}, payload) {
		commit(TYPE.ADD_PRODUCT, payload)
	},
	addCloud({commit}, value) {
		commit(TYPE.ADD_CLOUD, value)
	},
	setCurrentItem({commit}, payload) {
		commit(TYPE.SET_CURRENT_ITEM, payload)
	},
	setCurrentItemProp({commit}, payload) {
		commit(TYPE.SET_CURRENT_ITEM_PROP, payload)
	},
	setCurrentFormStep({commit}, value) {
		commit(TYPE.SET_CURRENT_FORM_STEP, value)
	},
	clearCurrentItem({commit}) {
		commit(TYPE.CLEAR_CURRENT_FORM_STEP)
	},
	setClientProp({commit}, payload) {
		commit(TYPE.SET_CLIENT_PROP, payload)
	},
	setPaymentToken({commit}, value) {
		commit(TYPE.SET_PAYMENT_TOKEN, value)
	},
	serverSetClient({state, commit, dispatch}) {
		client.getOrCreateClient(
			state.client_info,
			(response) => {
				console.log(response)
				commit(TYPE.SET_CLIENT_PROP, {prop: 'pk', data: response.data.pk})
			},
			(error) => {
				console.log("error")
			})
	}
}

const getters = {
	getCurrentFormStep: state => state.current_form_step,
	getFormSteps: state => state.steps,
	getProduct: state => sku => state.products[sku],
	getAllProducts: state => state.products,
	getCurrentItem: state => state.current_item,
	getCurrentItemProp: state => prop => state.current_item[prop],
	getClientInfo: state => state.client_info,
	getPaymentToken: state => state.payment_token,
}

export default {
	state,
	getters,
	mutations,
	actions
}