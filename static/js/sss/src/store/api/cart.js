import {URL_ROOT} from '../values'
import axios from 'axios'

const actions = {
	getOrCreateCart(cart_obj) {
		return axios.post(URL_ROOT + 'support/get-or-create-cart/', cart_obj)
		.then((response) => {
			return response
		})
		.catch((error) => {
			console.error(error)
		})
	},
	checkout(cart_obj, success) {
		axios.post(URL_ROOT + 'support/checkout/', cart_obj)
		.then((response) => {
			success(response)
		})
		.catch((error) => {
			console.error(error)
		})
	}
}

export default {
	...actions
}
