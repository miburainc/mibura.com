import {URL_ROOT} from '../values'
import axios from 'axios'

const actions = {
	sendPlaidCredentials(ach_account_id, ach_public_key) {
		return axios.post(
			URL_ROOT + 'support/plaid-credentials/', 
			{
				ach_account_id: ach_account_id,
				ach_public_key: ach_public_key
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
