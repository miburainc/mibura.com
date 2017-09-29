import * as TYPE from '../types'
import Vue from 'vue'

import {form_steps} from '../values'

const state = {
	steps: form_steps,
	products: {},
	current_item: {
		verified: false
	},
	current_form_step: 0,
	current_cloud_selection: 1,
	notifications: [],
	cloud_providers: []
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
	
	[TYPE.SET_CURRENT_FORM_STEP]: (state, value) => {
		state.current_form_step = value
	},
	[TYPE.CLEAR_CURRENT_FORM_STEP]: (state) => {
		Vue.set(state, "current_item", { verified: false })
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
	
	setCurrentCloudSelection({commit}, selection) {
		commit(TYPE.SET_CURRENT_CLOUD_SELECTION, selection)
	}
}

const getters = {
	getCloudProviders: state => state.cloud_providers,
	getCurrentFormStep: state => state.current_form_step,
	getFormSteps: state => state.steps,
	getProduct: state => sku => state.products[sku],
	getAllProducts: state => state.products,
	getCurrentItem: state => state.current_item,
	getCurrentItemProp: state => prop => state.current_item[prop],
	
	getCurrentCloudSelection: state => state.current_cloud_selection,
	getNotifications: state => state.notifications,
	filteredClouds: (state, getters, rootState) => {
		return state.cloud_providers.filter((cloud) => {
			let cart = rootState.Cart.cart
			for (let i=0; i<cart.length; i++) {
				if (cloud.name == cart[i].brand) {
					return false
				}
			}
			return true
		})
	}
}

export default {
	state,
	getters,
	mutations,
	actions
}