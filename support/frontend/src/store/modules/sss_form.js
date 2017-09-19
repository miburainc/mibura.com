import * as TYPE from '../types'
import Vue from 'vue'

import client from '../api/client'

import {form_steps} from '../values'

const state = {
	steps: form_steps,
	products: {},
	current_item: {
		verified: false
	},
	current_form_step: 0,
	current_cloud_selection: 1,
	client_info: {},
	payment_info: {},
	payment_token: "",
	notifications: [],
	cloud_providers: [],
	allow_form_submit: true,
	payment_processing: false,
}

const mutations = {
	[TYPE.SET_ALLOW_FORM_SUBMIT]: (state, value) => {
		state.allow_form_submit = value
	},
	[TYPE.SET_PAYMENT_PROCESSING]: (state, value) => {
		state.payment_processing = value
	},
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
	[TYPE.SET_PAYMENT_PROP]: (state, payload) => {
		Vue.set(state.payment_info, payload.prop, payload.data)
	},
	[TYPE.CLEAR_CURRENT_FORM_STEP]: (state) => {
		Vue.set(state, "current_item", { verified: false })
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
	[TYPE.SET_CLOUD_PROVIDERS]: (state, value) => {
		state.cloud_providers = value
	},
	[TYPE.ADD_NOTIFICATION]: (state, payload) => {
		state.notifications.splice(0, 0, payload)
		
		if(state.notifications.length > 1){
			state.notifications.pop()
		}
		
	},
	[TYPE.REMOVE_NOTIFICATION]: (state, index) => {
		state.notifications.splice(index, 1)
	}
}

const actions = {
	setAllowFormSubmit({commit}, value){
		commit(TYPE.SET_ALLOW_FORM_SUBMIT, value)
	},
	setPaymentProcessing({commit}, value){
		commit(TYPE.SET_PAYMENT_PROCESSING, value)
	},
	setCloudProviders({commit}, payload) {
		commit(TYPE.SET_CLOUD_PROVIDERS, payload)
	},
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
	setPaymentProp({commit}, payload) {
		commit(TYPE.SET_PAYMENT_PROP, payload)
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
	getPaymentProcessing: state => state.payment_processing,
	getAllowFormSubmit: state => state.allow_form_submit,
	getCloudProviders: state => state.cloud_providers,
	getCurrentFormStep: state => state.current_form_step,
	getFormSteps: state => state.steps,
	getProduct: state => sku => state.products[sku],
	getAllProducts: state => state.products,
	getCurrentItem: state => state.current_item,
	getCurrentItemProp: state => prop => state.current_item[prop],
	getClientInfo: state => state.client_info,
	getPaymentInfo: state => state.payment_info,
	getPaymentInfoProp: state => prop => state.payment_info[prop],	
	getCurrentCloudSelection: state => state.current_cloud_selection,
	getNotifications: state => state.notifications,
}

export default {
	state,
	getters,
	mutations,
	actions
}