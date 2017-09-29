<template>
	<div>
		<div id="stripe-payment-form" style="margin-top:15px;">
			<h2 class="text-center">{{ title }}</h2>
			<h4 class="text-center">{{ text }}</h4>
			<ul class="nav nav-tabs" style="min-width:325px;">
				<li role="presentation" :class="{active: payment_type=='card'}"><a style="cursor: pointer;" @click="switchTabs('card')">Credit Card</a></li>
				<li role="presentation" :class="{active: payment_type=='paypal'}"><a style="cursor: pointer;" @click="switchTabs('paypal')">PayPal</a></li>
				<li role="presentation" :class="{active: payment_type=='ach'}"><a style="cursor: pointer;" @click="switchTabs('ach')">Bank ACH</a></li>
				<li role="presentation" :class="{active: payment_type=='po'}"><a style="cursor: pointer;" @click="switchTabs('po')">P.O.</a></li>
				<!-- <li role="presentation" :class="{active: payment_type=='verify'}"><a style="cursor: pointer;" @click="switchTabs('verify')">Verify ACH</a></li> -->
				

			</ul>
			<div class="payment-box">

				<div v-show="payment_type=='card'" class="stripe-form-cc pad-10" style="position:relative;">

					<form-text-input 
					:class="{'error-border': getErrors[cc_fields.cardname.form.name]}" 
					:step="cc_fields.cardname" 
					id="cardName"></form-text-input>

					<label>Card Info</label>
					<div id="card-element" class="field" :class="{'error-border': cardError}">{{cardError}}</div>
					<div class="outcome" style="margin:0px 0px 10px 0px;" >
						<div class="error" role="alert"></div>
						<!--
						<div class="success"> 
						Success! Your Stripe token is <span class="token"></span>
						</div>
						-->
					</div>
					<div style="position:absolute;font-size:32px; text-align:center; margin: 0px -93px; left: 50%; color: #2f334c;">
						<i class="fa fa-cc-visa" aria-hidden="true"></i>
						<i class="fa fa-cc-mastercard" aria-hidden="true"></i>
						<i class="fa fa-cc-discover" aria-hidden="true"></i>
						<i class="fa fa-cc-amex" aria-hidden="true"></i>
					</div>
					<br><br>
				</div>

				<div v-show="payment_type=='paypal'" class="pad-10" style="position:relative;">

					<!-- <form-text-input 
					:class="{'error-border': getErrors[cc_fields.cardname.form.name]}" 
					:step="cc_fields.cardname" 
					id="cardName"></form-text-input> -->

					<label>PayPal</label>
					<div id="paypal-button-container"></div>
				</div>

				

				<!-- <div v-if="payment_type=='verify'" style="margin: 10px 0px 10px 0px;">
					<br><p><i style="color: #3285C4" class="fa fa-info-circle" aria-hidden="false"> &nbsp;</i>Enter the two payments that were put into your bank account and we can verify your bank account.</p><br>
					<form-text-input 
					:class="{'error-border': getErrors[ach_fields[3].form.name]}" 
					:step="ach_fields[3]"></form-text-input>
					<form-text-input 
					:class="{'error-border': getErrors[ach_fields[4].form.name]}" 
					:step="ach_fields[4]"></form-text-input>
				</div> -->

				<div v-show="payment_type=='po'" class="stripe-form-cc pad-10">

					<form-text-input 
					:class="{'error-border': getErrors[po_fields[0].form.name]}" 
					:step="po_fields[0]" 
					id="cardName"></form-text-input>

					
				</div>
				
				<div v-show="payment_type=='ach'" class="stripe-form-ach pad-5" style="margin-bottom:5px;">

					<form-text-input :step="ach_fields[0]"></form-text-input>
					
					<div class="container-fluid" style="border-top: 1px solid #8493A8; padding-top:15px; margin-top:10px; ">
						<div class="row">
							<div class="col-xs-12 col-md-5 plaid-button-container" style=" text-align:center;">
								<button 
								:class="{'btn-plaid-success': getAchPaymentToken != ''}"
								style="" v-on:keypress.enter.prevent type="button" v-show="payment_type=='ach'" id='linkButton' class="btn btn-lg btn-primary payment-button">{{ plaid_btn_text1 }}<br>{{ plaid_btn_text2 }}</button>
							</div>
							<div class="col-xs-12 col-md-2 text-center payment-or">
								<div class="line"></div>
								<div class="orText">or</div>
								<div class="line"></div>
							</div>
							<div class="col-xs-12 col-md-5">
								
								<form-text-input 
									:achToken="getAchPaymentToken != '' ? 'success' : 'failure'"
									style="margin-top:15px"
									:step="ach_fields[1]"></form-text-input>
								<form-text-input  
									:achToken="getAchPaymentToken != '' ? 'success' : 'failure'"
									:step="ach_fields[2]"></form-text-input>
								<input type="checkbox" name="accounttype" @click="(checked) => {setPaymentProp({prop: 'accounttype', data: checked.target.checked ? 'company' : 'individual'})}">
								This is a company account
								<br>
								<a role="button" data-toggle="modal" data-target="#achInfoModal" style="text-align: center; margin-bottom:0px; color:gray;"><i style="color: #3285C4" class="fa fa-info-circle" aria-hidden="false"> &nbsp; </i>What is this?</a>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div v-bind:style="buttonStyle" class="container-fluid" style="padding:0px"> 	
				
				
				<div class="col-xs-12" style="padding:0px; margin:0px;">
					<button v-on:keypress.enter.prevent :class="buttons[0].class" type="button"
				@click="(el) => {buttonAction(el, buttons[0].script)}" style="width:50%;white-space:normal;">
						{{form.buttons[0].label}}
					</button><button id="btn_review" v-on:keypress.enter.prevent @click="buttonContinue" :class="buttons[1].class" type="button" style="width:50%; white-space:normal;" :disabled="getPaymentProcessing">
						{{ !getPaymentProcessing ? buttons[1].label : "Processing"}} <i v-if="getPaymentProcessing" class="fa fa-circle-o-notch fa-spin" style="font-size:24px"></i>
					</button>
				</div>

				<!-- <button v-if="getPaymentProcessing" style="width:100%" class="btn btn-lg btn-success" disabled>
					Processing <i class="fa fa-circle-o-notch fa-spin" style="font-size:24px"></i>
				</button> -->
				
			</div>

			<div class="text-center">
				<img style="margin-top: 10px; margin-right: 5px;" :src="URL_ROOT+'static/images/comodo_secure_seal_76x26_transp.png'" alt="Comodo Secure">
				<img style="margin-top: 10px; margin-right: 5px;" :src="URL_ROOT+'static/images/powered_by_stripe@2x.png'" height="26" alt="Powered by Stripe">
			</div>
				

		</div>
	</div>
</template>

<script>

import {mapGetters, mapActions} from 'vuex'
import FormTextInput from '../FormTextInput.vue'
import {ValidateFormStep} from '../../scripts/functions.js'

import {URL_ROOT} from '../../store/values'

import { forEachValue } from '../../scripts/util'

import stripe from '../../store/stripe'

export default {
	components: {
		'form-text-input': FormTextInput
	},
	data() {
		return {
			stripe: stripe,
			title: "Payment",
			text: "We accept all major credit cards, Bank ACH, or if you already have an account with Mibura, simply create a purchase order here",
			URL_ROOT: URL_ROOT,
			elements: null,
			cards: null,
			payment_type: 'card',
			cardError: false,
			formErrors: false,
			title: "",
			text: "",
			cc_fields: {
				cardname: {
					placeholder: "Name on card",
					src: "",
					dest: "payment.cardname",
					required: true,
					validate: {
						type: "text",
						min: 3,
					},
					form: {
						type: "text",
						name: "cardname",
						class: "field",
					}
				}
			},
			ach_fields: [
				{
					placeholder: "Bank Customer Name",
					src: "",
					dest: "payment.bankcustomername",
					required: true,
					validate: {
						type: "text",
						min: 3,
					},
					form: {
						type: "text",
						name: "bankcustomername",
						class: "field",
					}
				},
				{
					placeholder: "Account Number",
					src: "",
					dest: "payment.accountnumber",
					required: true,
					validate: {
						type: "number",
						min: 6,
					},
					form: {
						type: "number",
						name: "accountnumber",
						class: "field",
					}
				},
				{
					placeholder: "Routing Number",
					src: "",
					dest: "payment.routingnumber",
					required: true,
					validate: {
						type: "number",
						min: 6,
					},
					form: {
						type: "number",
						name: "routingnumber",
						class: "field",
					}
				},
				{
					placeholder: "Verify Ammount #1",
					src: "",
					dest: "payment.verify1",
					required: true,
					validate: {
						type: "number",
						min: 2,
					},
					form: {
						type: "number",
						name: "verify1",
						class: "field",
					}
				},
				{
					placeholder: "Verify Ammount #2",
					src: "",
					dest: "payment.verify2",
					required: true,
					validate: {
						type: "number",
						min: 2,
					},
					form: {
						type: "number",
						name: "verify2",
						class: "field",
					}
				},
			],
			po_fields: [
				{
					placeholder: "P.O. Number",
					src: "",
					dest: "payment.ponumber",
					required: true,
					validate: {
						type: "text",
						min: 4,
					},
					form: {
						type: "text",
						name: "ponumber",
						class: "field",
					}
				}			
			],
			paypal_fields: [
			],
			buttons: [
				{
					label: "Back",
					class: "btn btn-lg btn-default",
					script: "back"
				},
				{
					label: "Continue",
					class: "btn btn-lg btn-success payment-button",
					script: "review"
				},
			],
			title: "Payment",
			text: "We accept all major credit cards, Bank ACH, or if you already have an account with Mibura, simply create a purchase order here",
			error: "",
			step: 3,
			buttonStyle: ""
		}
	},
	props: ['form', 'buttonAction'],
	methods: {
		...mapActions([
			'setPaymentProp',
			'setPaymentToken',
			'plaidSendCredentials',
			'clearError',
			'clearErrors',
			'setError',
			'setCurrentFormStep',
			'serverSetClient',
			'setPaymentProcessing',
			'createPaymentObject'
		]),
		sendplaidcredentials() {
			this.plaidSendCredentials()
				.then(() => {
					this.createPaymentObject({
						client_id: this.getClientInfo['pk'],
						cart_ref: this.getCartReference,
						payment_type: 'achplaid',
						token: this.getPaymentInfoProp('ach_payment_token')
					})
				})
		},
		switchTabs(newTab){
			this.payment_type = newTab
			this.clearErrors()
		},
		checkError(){
			return(true)
		},
		stripeSetOutcome(result) {
			var errorElement = document.querySelector('.error');
			errorElement.classList.remove('visible');

			var error = false
			if (result.token) {

				// Use the token to create a charge or a customer
				// https://stripe.com/docs/charges
				this.setPaymentToken(result.token.id);
				this.setPaymentProp({prop: 'cc_payment_token', data: result.token.id})
				setTimeout(function(){this.setPaymentProcessing(false)}, 400)

			} else if (result.error) {
				errorElement.textContent = result.error.message;
				errorElement.classList.add('visible');
				error = true
			}

			this.cardError = error
			
			return(error)
		},
		
		buttonContinue() {
			var extraDetails = {
				
			};

			var script = "submitpayment"

			var noFormErrors = true

			let errors = null

			if(this.payment_type == 'card'){
				
				let cardName = document.getElementById("cardname").value
				extraDetails['name'] = cardName

				errors = ValidateFormStep(this.cc_fields.cardname, cardName)
				if (errors["valid"] == false)
				{
					forEachValue(errors["errors"], (value, key) => {
						value.map((val) => {
							this.setError({key: key, value: value})
						})
					})

					noFormErrors = false
				}

				if(noFormErrors){
					this.stripe.createToken(this.card, extraDetails).then(this.stripeSetOutcome).then(() => {
						if(!this.cardError){
							this.createPaymentObject({
								client_id: this.getClientInfo['pk'],
								cart_ref: this.getCartReference,
								payment_type: 'creditcard',
								token: this.getPaymentInfoProp('cc_payment_token')
							})
							this.buttonAction(null, script)	
						}
					});
				}
			}
			else if(this.payment_type == 'ach'){

				let bankcustomername = document.getElementById("bankcustomername").value
				extraDetails['bankcustomername'] = bankcustomername

				console.log("error bankcustomername:", bankcustomername)

				errors = ValidateFormStep(this.ach_fields[0], bankcustomername)
				if (errors["valid"] == false)
				{
					forEachValue(errors["errors"], (value, key) => {
						value.map((val) => {
							this.setError({key: key, value: value})
						})
					})

					noFormErrors = false
				}

				if(this.getAchPaymentToken == ""){
					let accountNumber = document.getElementById("accountnumber").value
					extraDetails['accountnumber'] = accountNumber

					errors = ValidateFormStep(this.ach_fields[1], accountNumber)
					if (errors["valid"] == false)
					{
						forEachValue(errors["errors"], (value, key) => {
							value.map((val) => {
								this.setError({key: key, value: value})
							})
						})

						noFormErrors = false
					}

					let routingNumber = document.getElementById("routingnumber").value
					extraDetails['routingnumber'] = routingNumber



					errors = ValidateFormStep(this.ach_fields[2], routingNumber)
					if (errors["valid"] == false)
					{
						forEachValue(errors["errors"], (value, key) => {
							value.map((val) => {
								this.setError({key: key, value: value})
							})
						})

						noFormErrors = false
					}

					script = "submitach"

					if(noFormErrors){
						this.buttonAction(null, "submitach")
					}
				}
				else{
					if(noFormErrors){
						this.buttonAction(null, script)	
					}
				}
			}
			else if(this.payment_type == 'po'){

				console.log("payment_type: po")
				let ponumber = document.getElementById("ponumber").value

				errors = ValidateFormStep(this.po_fields[0], ponumber)
				if (errors["valid"] == false)
				{
					forEachValue(errors["errors"], (value, key) => {
						value.map((val) => {
							this.setError({key: key, value: value})
						})
					})

					noFormErrors = false
				}

				script = "sendponumber"

				if(noFormErrors){
					this.buttonAction(null, script)
				}
			}

			if(noFormErrors){
				setTimeout(()=>{if(!this.cardError){this.setPaymentProcessing(true)}}, 50)
			}
		}
	},
	mounted() {

		// PayPal

		paypal.Button.render({

            env: 'sandbox', // sandbox | production

            // PayPal Client IDs - replace with your own
            // Create a PayPal app: https://developer.paypal.com/developer/applications/create
            client: {
                sandbox: 'AZDxjDScFpQtjWTOUtWKbyN_bDt4OgqaF4eYXlewfBP4-8aqX3PiV8e1GWU6liB2CUXlkA59kJXE7M6R',
                production: '<insert production client id>'
            },

            // Show the buyer a 'Pay Now' button in the checkout flow
            commit: true,

            // payment() is called when the button is clicked
            payment: function(data, actions) {

                // Make a call to the REST api to create the payment
                return actions.payment.create({
                    payment: {
                        transactions: [
                            {
                                amount: { total: '0.01', currency: 'USD' }
                            }
                        ]
                    }
                });
            },

            // onAuthorize() is called when the buyer approves the payment
            onAuthorize: function(data, actions) {

                // Make a call to the REST api to execute the payment
                return actions.payment.execute().then(function() {
                    window.alert('Payment Complete!');
                });
            }

        }, '#paypal-button-container');

		// Plaid

		var linkHandler = Plaid.create({
			env: 'sandbox',
			clientName: 'MiBURA',
			key: '87d5d9538ea6876052c9f655c91df8',
			product: ['auth'],
			selectAccount: true,
			onSuccess: (public_token, metadata) => {
				// Send the public_token and account ID to your app server.
				// console.log('public_token: ' + public_token);
				// console.log('account ID: ' + metadata.account_id);
				// sendDataToBackendServer({
				//   public_token: public_token,
				//   account_id: metadata.account_id
				// });
				this.setPaymentProp({prop: 'ach_public_token', data: public_token})
				this.setPaymentProp({prop: 'ach_account_id', data: metadata.account_id})
				this.plaidSendCredentials()

				var extraDetails = {
				
				};

				var errors = null

				let bankcustomername = document.getElementById("bankcustomername").value
				extraDetails['bankcustomername'] = bankcustomername

				console.log("errors: bankcustomername", bankcustomername)

				errors = ValidateFormStep(this.ach_fields[0], bankcustomername)
				if (errors["valid"] == false)
				{
					forEachValue(errors["errors"], (value, key) => {
						value.map((val) => {
							this.setError({key: key, value: value})
						})
					})
				}

				console.log("plaid")
			},
			onExit: function(err, metadata) {
				// The user exited the Link flow.
				if (err != null) {
					// The user encountered a Plaid API error prior to exiting.
				}
			},
		});

		// Trigger the Link UI
		document.getElementById('linkButton').onclick = function() {
			linkHandler.open();
		};
		
		this.elements = this.stripe.elements();
		this.card = this.elements.create('card', {
			style: {
				base: {
					iconColor: '#548ebf',
					color: '#333333',
					lineHeight: '40px',
					fontWeight: 300,
					fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
					fontSize: '15px',

					'::placeholder': {
						color: '#888888',
					},
				},
			}
		});
		this.card.mount('#card-element');
		var self = this;
		
		this.card.on('change', (event) => {
			
			this.cardError = this.stripeSetOutcome(event);
			console.log(this.cardError)
		});

	},
	computed: {
		...mapGetters([
			'getErrors',
			'getAchPaymentToken',
			'getCurrentFormStep',
			'getPaymentProcessing',
			'getPaymentInfoProp',
			'getClientInfo',
			'getCartReference',
		]),

		plaid_btn_text1(){
			if(this.getAchPaymentToken == ""){
				return 'Login to'	
			}
			else{
				return 'Successfully'
			}
			
		},
		plaid_btn_text2(){
			if(this.getAchPaymentToken == ""){
				return 'Bank Account'
			}
			else{
				return 'Linked to Bank'
			}
		}
	}
}

</script>

<style lang="scss" scoped>

.plaid-button-container > button {
	margin: 30px 0px 0px 18%;
	padding: 30px; 
}


@media (max-width: 991px) {
	.payment-or {
		display: none;
	}
	.plaid-button-container > button {
		margin: 0px;
		padding: 30px; 
	}
}

.btn-plaid-success {
	padding: 10px 20px;
	color: black!important;
	cursor: initial!important;
	background: #5cb85c!important;
	border: 1px solid #00a25c;
	transition: 0.2s background, 0.2s color;

	&:hover {
		padding: 10px 20px;
		color: black!important;
		cursor: initial!important;
		border-color: #00a25c!important;
		background: #5cb85c!important;
		// border: 1px solid #FFFFFF;
	}
	&:focus {
		color: black!important;
		cursor: initial!important;
	}
}

label {
	color: #333;
}

div.line{
	width: 0px;
	height: 52px;
	position:relative;

	margin: 10px auto;
	border-right: 1px solid #8493A8;
	
	
}

.payment-box {
	border-radius: 2px;
	border-top: 1px solid #8493A8;
}

.nav-tabs {
	border: none;
}

.nav-tabs li a {
	color: black;
}

.nav-tabs li.active a {
	border: 1px solid #8493A8;
	background: rgba(255,255,255,0.1);
	border-bottom: none;
}

.nav-tabs li a:hover {
	border: 1px solid #8493A8;
	border-bottom: 1px solid #8493A8;
	background: rgba(255,255,255,0.2);
	color: black;
}

.nav-tabs li a:active, .nav-tabs li a:visited {
	color: black;
}

</style>