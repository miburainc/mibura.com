import {URL_ROOT} from '../values'
import axios from 'axios'

const actions = {
	getOrCreateClient(client_obj) {
		return axios.post(URL_ROOT + 'support/get-or-create-client/', client_obj)
		.then((response) => {
			return response
		})
		.catch((error) => {
			console.error(error)
		})
	},
	getOrCreateSubscription(client_obj) {
		return axios.post(URL_ROOT + 'support/get-or-create-subscription/', client_obj)
		.then((response) => {
			return response
		})
		.catch((error) => {
			console.error(error)
		})
	}
}

export default {
	...actions
}