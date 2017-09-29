import * as TYPE from '../types'
import Vue from 'vue'

import client from '../api/client'

const state = {
	client_info: {},
}

const mutations = {
	[TYPE.SET_CLIENT_PROP]: (state, payload) => {
		Vue.set(state.client_info, payload.prop, payload.data)
	},
	[TYPE.SET_CLIENT]: (state, payload) => {
		Vue.set(state, 'client_info', payload)
	},
	[TYPE.CLEAR_CLIENT]: (state, payload) => {
		Vue.set(state, 'client_info', {})
	},
}

const getters = {
	getClientInfo: state => state.client_info,
}

const actions = {
	setClient({commit}, payload){
		commit(TYPE.SET_CLIENT, payload)
	},
	setClientProp({commit}, payload) {
		commit(TYPE.SET_CLIENT_PROP, payload)
	},
	serverSetClient({state, commit, dispatch}) {
		return client.getOrCreateClient(
			state.client_info).then(response => {
				commit(TYPE.SET_CLIENT_PROP, {prop: 'pk', data: response.data})
			})
	},
}

export default {
	state,
	mutations,
	getters,
	actions
}