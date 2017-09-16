import {URL_ROOT} from '../values'
import axios from './api-config'

const actions = {
	postAchCredentials(client_id, stripeAchToken) {
		return axios.post(
			URL_ROOT + 'support/ach-credentials/', 
			{
				client_id: client_id,
				stripeAchToken: stripeAchToken
			}
		)
		.then((response) => {
			return response
		})
		.catch((error) => {
			console.error(error)
		})
	},
	postAchVerify(client_id, ach_verify_amt1, ach_verify_amt2) {
		return axios.post(
			URL_ROOT + 'support/ach-verify/', 
			{
				client_id: client_id,
				ach_verify_amt1: ach_verify_amt1,
				ach_verify_amt2: ach_verify_amt2
			}
		)
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
