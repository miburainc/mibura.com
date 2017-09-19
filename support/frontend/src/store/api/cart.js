import {API_ROOT,URL_ROOT} from '../values'
import axios from './api-config'

const actions = {
	getCart(reference){
		return axios.post(URL_ROOT + 'support/get-cart/', reference).then((response) => {
			return response
		}).catch((error) => {
			console.error(error)
			return error
		})
	},
	getOrCreateCart(cart_obj) {
		return axios.post(URL_ROOT + 'support/get-or-create-cart/', cart_obj)
		.then((response) => {
			return response
		})
		.catch((error) => {
			console.error(error)
			return error
		})
	},
	api_checkout(cart_obj) {
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
	},
	sendAchRequest(payload){
		
	}
}

export default {
	...actions
}
