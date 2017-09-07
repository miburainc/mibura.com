import {API_ROOT,URL_ROOT} from '../values'
import axios from './api-config'

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
	checkout(cart_obj) {
		return axios.post(URL_ROOT + 'support/checkout/', cart_obj)
		.then((response) => {
			return response
		})
		.catch((error) => {
			console.error(error)
		})
	},
	sendQuoteEmail(cart_ref) {
		return axios.post(URL_ROOT + 'support/send-quote-email/', {cart_ref: cart_ref})
		.then((response) => {
			return response
		})
		.catch((error) => {
			console.error(error)
		})
	},
	serverGetDiscounts() {
		return axios.get(API_ROOT+'discounts')
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
