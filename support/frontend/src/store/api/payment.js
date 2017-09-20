import {URL_ROOT} from '../values'
import axios from './api-config'

const actions = {
	sendPaymentPoNumber(payload) {
		return axios.post(URL_ROOT + 'support/create-purchase-order/', payload)
		.then((response) => {
			return response
		})
		.catch((error) => {
			console.error(error)
		})
	},
}

export default {
	...actions
}