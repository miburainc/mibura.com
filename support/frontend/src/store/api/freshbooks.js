import {URL_ROOT, API_ROOT} from '../values'
import axios from './api-config'

const actions = {
	getEstimatePDF(client, cart_ref) {
		// console.log("freshbooks.js__getEstimatePDF")
		// console.log("post")
		let data_raw = {
			'client': client,
			'cart_reference': cart_ref
		}
		let data_obj = JSON.stringify(data_raw)

		return axios({
			method: 'post',
			url: URL_ROOT + 'support/get-estimate-pdf/',
			data: data_obj,
			responseType: 'arraybuffer'
		}).then((response) => {
			return response
		}).catch((error) => {
			console.error(error)
		})
	},
	request_past_estimate(estimate_ref) {
		return axios({
			method: 'post',
			url: URL_ROOT + 'support/get-previous-estimate/',
			data: {'estimate_ref': estimate_ref},
		}).then((response) => {
			return response
		}).catch((error) => {
			console.error(error)
		})
	}
}

export default {
	...actions
}
