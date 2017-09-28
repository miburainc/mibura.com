<template>
	<div id="app" class="container-fluid">
		<!-- Confirm Terms and conditions -->
		<div class="modal fade" id="termsModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Terms and conditions</h4>
					</div>
					<div class="modal-body">
						<div id="pdf">
							<object width="100%" height="500" type="application/pdf" id="pdf_content">
							
							</object>
						</div>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
						<button type="button" class="btn btn-primary" @click="setAcceptedTerms(true)" data-dismiss="modal">Accept</button>
					</div>
				</div>
			</div>
		</div>
		<!-- Info for ach payment -->
		<div class="modal fade" id="achInfoModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Payment by ACH</h4>
					</div>
					<div class="modal-body">
						<p>
							In order to pay with a bank account number we must first confirm your account.  To do this we will deposit two small ammounts into your bank account.  Once you recieve the payments you can come back to this site and tell us the ammounts to confirm that you are the owner of the account.  To speed up the process you can get an estimate and use your cart reference code to quickly return to where you left off.  If you have any questions, please contact us at 1-800-862-5144.
						</p>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
					</div>
				</div>
			</div>
		</div>
		<!-- Popup when user submits ach using account number and routing number -->
		<div class="modal fade" id="achSubmitModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Payment by ACH</h4>
					</div>
					<div class="modal-body">
						<p>
							In order for us to process your payment we will need to confirm that your account is valid. To do this we will deposit two small ammounts into your bank account.  Once you recieve the payments you can come back to this site and enter the ammounts to finish the confirmation.  To speed up the process you can get an estimate and use your cart reference code to quickly return to where you left off.  After this you will be able to review your order and choose to initiate payment.  
							<br><br>
							We will send you an email with a quote of your order and a link to return to confirm your payment ammounts.
							<br><br>
							If you have any questions, please contact us at 1-800-862-5144.
						</p>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Back</button>
						<button type="button" class="btn btn-primary" @click="confirmAch" data-dismiss="modal">Continue</button>
					</div>
				</div>
			</div>
		</div>
		<div class="modal fade" id="returnModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Already have a quote?</h4>
					</div>
					<div class="modal-body">
						<p>
							Thank you for returning to Mibura Smart Support.  Please enter the Smart Support Cart ID located at the bottom of your estimate PDF.  
						</p>
						<input class="form-control" placeholder="Quote ID" id="quoteIdInput" style="color:black;" v-on:keyup.enter="submitQuoteId">
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Back</button>
						<button type="button" class="btn btn-primary" @click="submitQuoteId">Continue</button>
					</div>
				</div>
			</div>
		</div>
		<div class="modal fade" id="verifyModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">ACH Verification</h4>
					</div>
					<div class="modal-body">
						<p>
							Please enter the ACH verification payment ammounts that were deposited into your bank account.  
						</p>
						<input class="form-control" :class="{'error-border': verifyError1}" placeholder="Ammount #1" id="verify1" style="color:black;" v-on:keyup.enter="submitVerification" @keyup="(el) => {
								ValidateFormStepFunction({
												placeholder: 'Ammount #1',
												src: 'verify1',
												dest: 'verify.1',
												required: true,
												form: {
													type: 'number',
													name: '1',
												},
												validate: {
													type: 'number',
													min: 2,
												}
											}, el.target.value)}">
						<input class="form-control" :class="{'error-border': verifyError2}" placeholder="Ammount #2" id="verify2" style="color:black;" v-on:keyup.enter="submitVerification"@keyup="(el) => {
								ValidateFormStepFunction({
												placeholder: 'Ammount #2',
												src: 'verify2',
												dest: 'verify.2',
												required: true,
												form: {
													type: 'number',
													name: '2',
												},
												validate: {
													type: 'number',
													min: 2,
												}
											}, el.target.value)}">
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Back</button>
						<button type="button" class="btn btn-primary" @click="submitVerification">Submit</button>
					</div>
				</div>
			</div>
		</div>
		<div class="modal fade" id="returnSuccessModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Returning Customer</h4>
					</div>
					<div class="modal-body">
						<div v-if="cartLoaded">
							<h4>Your quote has been loaded successfully!</h4>
						</div>
						<div v-else-if="cartLoadError">
							<h4>Invalid Cart Reference Code, try again.</h4>
							<input class="form-control" placeholder="Quote ID" id="quoteIdInput2" style="color:black;" v-on:keyup.enter="submitQuoteId2">
						</div>
						<div v-else>
							<h4>Processing</h4>
							<button class="btn btn-lg btn-success" type="button" disabled="true">
								<i class="fa fa-circle-o-notch fa-spin" style="font-size:24px"></i>
							</button>
						</div>
					</div>
					<div class="modal-footer">
						<!-- <button v-if="getEstimatePDF" class="btn btn-success" id="verify-ach" @click="goToVerify">Verify ACH</button>
						<button v-if="getEstimatePDF" type="button" class="btn btn-primary" @click="goToPayment">Go to Payment</button>-->
						<button v-if="cartLoaded" class="btn btn-success" id="verify-ach" @click="goToVerify">Verify ACH</button>
						<button v-if="cartLoaded" type="button" class="btn btn-primary" @click="goToPayment">Go to Payment</button>
						<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
						<button v-if="cartLoadError" type="button" class="btn btn-info" @click="submitQuoteId2">Retry</button>
					</div>
				</div>
			</div>
		</div>
		<!-- Input Estimate ID -->
		<div class="modal fade" id="estimateIdModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Open Estimate</h4>
					</div>
					<div class="modal-body" style="overflow-y: scroll;">
						<h4>Input Estimate ID</h4>
						<input style="color: #000000;" type="text" name="estimate_id" class="form-control" v-model="estimate_id" autofocus>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
						<button type="button" class="btn btn-primary" @click="requestPastQuote">Request</button>
					</div>
				</div>
			</div>
		</div>
		<!-- Price Confirmation -->
		<div class="modal fade" id="cartPriceModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Terms and conditions</h4>
					</div>
					<div class="modal-body" style="overflow-y: scroll;">
						
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
						<button type="button" class="btn btn-primary">Submit Payment</button>
					</div>
				</div>
			</div>
		</div>
		<!-- PDF Quote modal -->
		<div class="modal fade" id="pdfModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Download or Print Estimate</h4>
					</div>
					<div class="modal-body">
						<div v-if="getEstimatePDF">
							<h4>Your estimate is ready!</h4>
							<div id="pdf">
  								<object width="100%" height="500" type="application/pdf" :data="getEstimatePDF" id="pdf_content">
    								<p>Insert your error message here, if the PDF cannot be displayed.</p>
  								</object>
							</div>
						</div>
						<div v-else>
							<h4>Processing</h4>
							<button class="btn btn-lg btn-success" type="button" disabled="true">
								<i class="fa fa-circle-o-notch fa-spin" style="font-size:24px"></i>
							</button>
						</div>
					</div>
					<div class="modal-footer">
						<a v-if="getEstimatePDF" :download="'Mibura_SmartSupport_Estimate-' + localDate(new Date()) + '.pdf'" class="btn btn-success" id="pdf-link" target="_blank" :href="getEstimatePDF">Download PDF</a>
						<button v-if="getEstimatePDF" type="button" class="btn btn-primary" @click="emailQuote">Receive in Email</button>
						<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
					</div>
				</div>
			</div>
		</div>
		<!-- Call or Chat -->
		<div class="modal fade" id="chatModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Contact Sales</h4>
					</div>
					<div class="modal-body text-center">
						<h3>Cart Reference Code<br>{{getCartReference}}</h3>
					</div>
					<div class="modal-footer">
						<a href="tel:1-800-862-5144" class="btn btn-primary">Call Now <i class="fa fa-phone" aria-hidden="true"></i></a>
						<button type="button" class="btn btn-info openchat">Chat Now <i class="fa fa-comment" aria-hidden="true"></i></button>
						<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
					</div>
				</div>
			</div>
		</div>


		<!-- Modal Components -->
		<change-personal-modal></change-personal-modal>
		<unverified-items-modal></unverified-items-modal>



		<div v-if="!getPurchaseSuccess" class="notifications-container" style="padding: 0 5px;z-index: 5;">
			<notification v-for="(notification, index) in getNotifications" :data="notification" :index="index" :key="index"></notification>
		</div>

		<div v-if="getPurchaseSuccess" class="row">
			<success-screen></success-screen>
		</div>
		<div v-else class="row">
			<div class="col-xs-12">
				<progressbar></progressbar>
			</div>
			
			<div id="support-form" class="app-move-down col-xs-10 col-xs-offset-1 col-md-8 col-md-offset-0 col-lg-7 col-lg-offset-1">
				<support-form class="pad-10"></support-form>
			</div>
			<div id="side_cart_container" class=" app-move-down side-cart col-xs-12 col-md-4 col-lg-4" >
				<support-cart></support-cart>
			</div>
		</div>
	</div>
</template>

<script>

import SupportForm from './components/Form.vue'
import SupportCart from './components/Cart.vue'
import SuccessScreen from './components/SuccessScreen.vue'
import Notification from './components/Notification.vue'
import Progressbar from './components/ProgressBar.vue'

import ChangePersonalModal from './modals/ChangePersonalModal.vue'
import UnverifiedItemsModal from './modals/UnverifiedItemsModal.vue'

import {toJSONLocal} from './scripts/functions'

import {mapActions,mapGetters} from 'vuex'

import {ValidateFormStep} from './scripts/functions.js'

import { forEachValue } from './scripts/util'

import cart from './store/api/cart'

import axios from './store/api/api-config'

export default {
	name: 'app',
	data () {
		return {
			estimate_id: '',
			stripe: null,
			verifyError1: false,
			verifyError2: false,
			cartLoaded: false,
			cartLoadError: false
		}
	},
	components: {
		SupportForm,
		SupportCart,
		SuccessScreen,
		Notification,
		Progressbar,
		ChangePersonalModal,
		UnverifiedItemsModal,
	},
	computed: {
		...mapGetters([
			'getCartReference',
			'getPurchaseSuccess',
			'getEstimatePDF',
			'getNotifications',
			'getAPIRoot',
			'getClientInfo',
			'getPaymentInfo',
			'getCart',
			'getCartChanged',
			
		]),
		isCartLoaded(){
			return this.cartLoaded
		}
	},
	methods: {
		...mapActions([
			'setCategoryMultipliers',
			'setDiscounts',
			'setAcceptedTerms',
			'ServerRequestPastEstimate',
			'sendQuoteEmail',
			'setCloudProviders',
			'setCurrentFormStep',
			'setEstimatePdfFile',
			'achSendCredentials',
			'serverGetEstimatePdf',
			'serverSetClient',
			'saveCart',
			'setPaymentProp',
			'achSendVerify',
			'setCart',
			'setClient',
			'setClientProp'
		]),
		submitQuoteId(){

			var data = {
				// client_id: this.getClientInfo['pk'],
				reference: document.getElementById('quoteIdInput').value,
			}

			var newCart = cart.getCart(data).then((response) => {
				if(response['response'] != null){
					console.log(response)
					this.cartLoaded = true
					data = response.response.data
					console.log(data)
					let payload = {
						'items': data.items,
						'id': data.cart.id,
						'reference': data.cart.reference,
						'plan': data.cart.plan
					}

					this.setCart(payload)
					let client = JSON.parse(data.client)
					console.log(client)
					Object.keys(client).map((prop) => {
						console.log(prop)
						this.setClientProp({
							'prop': prop,
							'data': client[prop]
						})
					})
					
				}
				else{
					this.cartLoadError = true
				}
			})
			
			$('#returnModal').modal('toggle')
			$('#returnSuccessModal').modal('show')
			
		},
		submitQuoteId2(){

			var data = {
				reference: document.getElementById('quoteIdInput2').value,
			}

			var newCart = cart.getCart(data).then((response) => {
				if(response['response'] != null){
					this.cartLoaded = true
				}
				else{
					this.cartLoadError = true
					document.getElementById('quoteIdInput2').value = ""
				}
			})
		},
		goToVerify(){
			$('#returnSuccessModal').modal('toggle')
			$('#verifyModal').modal('show')
		},
		goToPayment(){
			console.log("LOAD CUSTOMER'S ESTIMATE DATA INTO STATE AND GO TO PAYMENT PAGE")
			$('#returnSuccessModal').modal('toggle')
			this.setCurrentFormStep(6)
		},
		submitVerification(){
			let v1 = document.getElementById('verify1').value
			let v2 = document.getElementById('verify2').value

			let format1 = {
				placeholder: "Ammount #1",
				src: "verify1",
				dest: "verify.1",
				required: true,
				form: {
					type: "number",
					name: "verify1",
				},
				validate: {
					type: "number",
					min: 2,
				}
			}
			let format2 = {
				placeholder: "Ammount #2",
				src: "verify2",
				dest: "verify.2",
				required: true,
				form: {
					type: "number",
					name: "verify2",
				},
				validate: {
					type: "number",
					min: 2,
				}
			}
			var errors = null

			var allGood = true

			errors = ValidateFormStep(format1, v1)
			if(errors.valid == false){
				console.log("error1")
				allGood = false
				this.verifyError1 = true
			}

			errors = ValidateFormStep(format2, v2)
			if(errors.valid == false){
				console.log("error2")
				allGood = false
				this.verifyError2 = true
			}

			if(allGood){
				$('#verifyModal').modal('toggle')
				this.setPaymentProp({prop: 'verify1', data: v1})
				this.setPaymentProp({prop: 'verify2', data: v2})
				this.achSendVerify()
			}
		},
		ValidateFormStepFunction(step, value){
			let errors = ValidateFormStep(step, value)

			if(errors['valid'] == true){
				if(step.form.name == '1'){
					this.verifyError1 = false
				}
				else if(step.form.name == '2'){
					this.verifyError2 = false
				}
			}
		},
		emailQuote() {
			this.sendQuoteEmail()
		},
		requestPastQuote() {
			this.ServerRequestPastEstimate(this.estimate_id)
		},
		localDate(date) {
			return toJSONLocal(date)
		},
		confirmAch(){

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
		}
	},
	mounted() {
		setTimeout(() => {
			this.stripe = Stripe('pk_test_jW4CJTGamhoH2cCxQljIKiwd');
		}, 1000)
		
		axios.get(this.getAPIRoot + 'cloud/')
			.then((response) => {
				console.log(response)
				this.setCloudProviders(response.data.results)
			})
			.catch((error) => {
				console.error(error)
			})
		this.setCategoryMultipliers()
		this.setDiscounts()
	}
}
</script>

<style lang="scss">

.btn-success {
	background-color: #2d85bf;
	border-color: #2d81ae;

	&:hover {
		background-color: #389fd5;
		border-color: #2d85bf;
	}

	&:active, &:focus, &:visited {
		background-color: #2d85bf!important;
		border-color: #2d81ae;
	}
}

.notifications-container {
	position: absolute;
	top: 80px;
	left: 0px;
	right: 0px;
}

#app {
	padding-top: 40px;
}

h1, h2, h3, h4 {
	margin: 0;
}

.btn-2, .btn-3, .btn-4 .btn-3-round .btn-2-round {
	width: 100%;
}

.btn-4 .btn {
	width: 24.95%;
} 

.btn-3 button.btn {
	margin: 0;
	margin-left: 0!important;
	border-radius: 0;
	width: 33.33%;
} 

.btn-3-round button.btn {
	margin: 0;
	margin-left: 0!important;
	width: 33.33%;
}

.btn-2 .btn {
	margin: 0;
	margin-left: 0!important;
	border-radius: 0;
	width: 50%!important;
}

.btn-2-round .btn {
	margin: 0;
	margin-left: 0!important;
	width: 50%!important;
}

.btn-plan {
	width: 33.33%;
	padding: 10px;
	border: 0;
}

.mobile-cart {
	display: none;
}

#side_cart {
	margin-top: 55px;
	-webkit-box-shadow: 2px 10px 20px 1px rgba(0,0,0,0.3);
	-moz-box-shadow: 2px 10px 20px 1px rgba(0,0,0,0.3);
	box-shadow: 2px 10px 20px 1px rgba(0,0,0,0.3);
}

.modal .modal-body {
    max-height: 420px;
    overflow-y: auto;
}

#support-form {
	margin-top: 45px;
	display: block;
	z-index: 0;
	min-height: 80%;
	min-height: 80vh;
}

.error-border{
	border-color: #ff3434!important;

	&:focus {
		border-color: red!important;
    -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 8px rgba(255, 52, 52, 0.6);
    box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 8px rgba(255, 52, 52, 0.6);
    	
	}
}


</style>
