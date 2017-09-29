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
	serverCreatePayment(payload) {
		return axios.post(URL_ROOT + 'support/create-payment-object/', payload)
		.then((response) => {
			return response
		})
		.catch((error) => {
			console.error(error)
			return error
		})
	},
	serverStartACH(){
		//finish submission of ach
		let payload = {
			'cart_ref': null,
			'accountnumber': this.getPaymentInfo['accountnumber'],
			'bankname': this.getPaymentInfo['bankcustomername'],
			'bankphone': this.getPaymentInfo['bankphone'],
			'routingnumber': this.getPaymentInfo['routingnumber']
		}

		this.stripe.createToken('bank_account', {
			country: 'us',
			currency: 'usd',
			routing_number: this.getPaymentInfo['routingnumber'],
			account_number: this.getPaymentInfo['accountnumber'],
			account_holder_name: this.getPaymentInfo['bankcustomername'],
			account_holder_type: this.getPaymentInfo['accounttype'],
		}).then((results) => {
			// handle result.error or result.token
			console.log(results.token)
			this.setPaymentProp({ prop: 'banktoken', data: results.token.id})
			this.setPaymentProp({ prop: 'bankname', data: results.token.bank_account.bank_name})

			// Reset pdf to nothing
			this.setEstimatePdfFile(null);
			// Send request for new pdf file
			this.serverSetClient().then(() => {
				this.saveCart(this.getClientInfo)
			// }).then(() => {
				// this.serverGetEstimatePdf()
			}).then(() => {
				payload['cart_ref'] = this.getCartReference
				console.log("SEND PAYLOAD TO API ENDPOINT")
				console.log(payload)
				this.achSendCredentials(this.getPaymentInfo['banktoken'])
			})
			
		});


		
		
		
		//GO TO SUCCESS PAGE
	},
}

export default {
	...actions
}