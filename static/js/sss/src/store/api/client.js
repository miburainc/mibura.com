import {URL_ROOT} from '../values'
import axios from 'axios'

const actions = {
	getOrCreateClient(client_obj, success, error) {
		axios.post(URL_ROOT + 'support/get-or-create-client/', client_obj)
		.then((response) => {
			success(response)
		})
		.catch((error) => {
			console.error(error)
			error(error)
		})
	},
	getOrCreateSubscription(client_obj, success, error) {
		axios.post(URL_ROOT + 'support/get-or-create-subscription/', client_obj)
		.then((response) => {
			success(response)
		})
		.catch((error) => {
			console.error(error)
			error(error)
		})
	}
}

export default {
	...actions
}