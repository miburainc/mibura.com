import * as TYPE from '../types'
import Vue from 'vue'

import client from '../api/client'

import {form_steps} from '../values'

const state = {
	steps: form_steps,
	products: {},
	current_item: {},
	current_form_step: 0,
	current_cloud_selection: 1,
	client_info: {},
	payment_token: "",
	notifications: [
		{message: "test!", type: "success"},
		{message: "If you upgrade to gold, you get cloud support included for FREE!", type: "info"},
		{message: "test!", type: "warning"},
		{message: "test!", type: "danger"}
	],
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
	[TYPE.SET_CLIENT]: (state, payload) => {
		Vue.set(state, 'client_info', payload)
	},
	[TYPE.CLEAR_CLIENT]: (state, payload) => {
		Vue.set(state, 'client_info', {})
	},
	[TYPE.SET_CURRENT_CLOUD_SELECTION]: (state, selection) => {
		state.current_cloud_selection = selection
	},
	[TYPE.ADD_NOTIFICATION]: (state, payload) => {
		state.notifications.push(payload)
	},
	[TYPE.REMOVE_NOTIFICATION]: (state, index) => {
		state.notifications.splice(index, 1)
	}
}

const actions = {
	addNotification({commit}, payload) {
		commit(TYPE.ADD_NOTIFICATION, payload)
	},
	removeNotification({commit}, index) {
		commit(TYPE.REMOVE_NOTIFICATION, index)
	},
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
		return client.getOrCreateClient(
			state.client_info).then(response => {
				commit(TYPE.SET_CLIENT_PROP, {prop: 'pk', data: response.data})
			})
	},
	setCurrentCloudSelection({commit}, selection) {
		commit(TYPE.SET_CURRENT_CLOUD_SELECTION, selection)
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
	getCurrentCloudSelection: state => state.current_cloud_selection,
	getNotifications: state => state.notifications,
}

export default {
	state,
	getters,
	mutations,
	actions
}