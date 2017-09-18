<template>
	<div id="stripe-payment-form">
		<ul class="nav nav-tabs" style="min-width:325px;">
			<li role="presentation" :class="{active: payment_type=='card'}"><a style="cursor: pointer;" @click="switchTabs('card')">Credit Card</a></li>
			<li role="presentation" :class="{active: payment_type=='ach'}"><a style="cursor: pointer;" @click="switchTabs('ach')">Bank ACH</a></li>
			<li role="presentation" :class="{active: payment_type=='verify'}"><a style="cursor: pointer;" @click="switchTabs('verify')">Verify ACH</a></li>
		</ul>
		<div class="payment-box">

			<div v-show="payment_type=='card'" class="stripe-form-cc pad-10">

				<form-text-input 
				:class="{'error-border': getErrors[form.data[0].form.name]}" 
				:step="form.data[0]" 
				id="cardName"></form-text-input>

				<label>Card Info</label>
				<div id="card-element" class="field" :class="{'error-border': cardError}"></div>
				<div class="outcome" style="margin:0px 0px 10px 0px;" >
					<div class="error" role="alert"></div>
					<!--
					<div class="success"> 
					Success! Your Stripe token is <span class="token"></span>
					</div>
					-->
				</div>
			</div>

			<div v-if="payment_type=='verify'" style="margin: 10px 0px 10px 0px;">
				<br><p><i style="color: #3285C4" class="fa fa-info-circle" aria-hidden="false"> &nbsp;</i>Enter the two payments that were put into your bank account and we can verify your bank account.</p><br>
				<form-text-input 
				:class="{'error-border': getErrors[form.data[4].form.name]}" 
				:step="form.data[4]"></form-text-input>
				<form-text-input 
				:class="{'error-border': getErrors[form.data[5].form.name]}" 
				:step="form.data[5]"></form-text-input>
			</div>
			
			<div v-show="payment_type=='ach'" class="stripe-form-ach pad-10" style="margin-bottom:5px;">

				<form-text-input :step="form.data[1]"></form-text-input>
				
				<div class="container-fluid" style="border-top: 1px solid #8493A8; padding-top:15px; margin-top:10px; min-width:590px;">
					<div class="row">
						<div class="col-xs-5" style=" text-align:center;">
							<button 
							:class="{'btn-plaid-success': getAchPaymentToken != ''}"
							style="margin: 30px 0px 0px 18%; padding: 30px;" v-on:keypress.enter.prevent type="button" v-show="payment_type=='ach'" id='linkButton' class="btn btn-lg btn-outline-info payment-button">{{ plaid_btn_text1 }}<br>{{ plaid_btn_text2 }}</button>
						</div>
						<div class="col-xs-2 text-center">
							<div class="line"></div>
							<div class="orText">or</div>
							<div class="line"></div>
						</div>
						<div class="col-xs-5">
							
							<form-text-input 
								:achToken="getAchPaymentToken != '' ? 'success' : 'failure'"
								id="accountNumber" 
								style="margin-top:15px"
								:step="form.data[2]"></form-text-input>
							<form-text-input  
								:achToken="getAchPaymentToken != '' ? 'success' : 'failure'"
								id="routingNumber" 
								:step="form.data[3]"></form-text-input>
							<input type="checkbox" name="accounttype" @click="(checked) => {setPaymentProp({prop: 'accounttype', data: checked.target.checked ? 'company' : 'individual'})}">
							This is a company account
							<br>
							<a role="button" data-toggle="modal" data-target="#achInfoModal" style="text-align: center; margin-bottom:0px; color:gray;"><i style="color: #3285C4" class="fa fa-info-circle" aria-hidden="false"> &nbsp; </i>What is this?</a>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div v-bind:style="form.buttonStyle" class="container-fluid" style="padding:0px"> 	
			<div class="col-xs-12 col-md-6" style="padding:0px; margin:0px;"><button v-on:keypress.enter.prevent style="width:100%; white-space: normal;" :class="form.buttons[0].class" type="button"
			@click="(el) => {buttonAction(el, form.buttons[0].script)}">{{form.buttons[0].label}}</button></div><div class="col-xs-12 col-md-6" style="padding:0px; margin:0px;"><button id="btn_review" style="width:100%; white-space: normal;" v-on:keypress.enter.prevent :class="form.buttons[1].class" type="button" >{{form.buttons[1].label}}</button></div>
			
		</div>
	</div>
</template>

<script>

import {mapGetters, mapActions} from 'vuex'
import FormTextInput from '../FormTextInput.vue'
import {ValidateFormStep} from '../../scripts/functions.js'

import { forEachValue } from '../../scripts/util'

export default {
	components: {
		'form-text-input': FormTextInput
	},
	data() {
		return {
			payment_type: 'card',
			cardError: false,
		}
	},
	props: ['form', 'buttonAction'],
	methods: {
		...mapActions([
			'setPaymentProp',
			'setPaymentToken',
			'setStripeProp',
			'plaidSendCredentials',
			'clearError',
			'clearErrors',
			'setError',
			'setCurrentFormStep',
			'serverSetClient'
		]),
		sendplaidcredentials() {
			this.plaidSendCredentials()
		},
		switchTabs(newTab){
			this.payment_type = newTab
			this.clearErrors()
			// if(newTab == 'card'){
			// 	for (i = 0; i < form.data.length; i++) { 
			// 		clearErrors()
			// 	    if(i <= 1){
			// 	    	ValidateFormStep(form.data[i], document.getElementById(form.data[i]).value)
			// 	    }
			// 	}
			// }
			// else if(newTab == 'ach'){
			// 	for (i = 0; i < form.data.length; i++) { 
			// 		clearErrors()
			// 	    if(i >= 2) && (i <= 5){
			// 	    	ValidateFormStep(form.data[i], document.getElementById(form.data[i]).value)
			// 	    }
			// 	}
			// }
			// else if(newTab == 'verify'){
			// 	for (i = 0; i < form.data.length; i++) { 
			// 		clearErrors()
			// 	    if(i >= 6){
			// 	    	ValidateFormStep(form.data[i], document.getElementById(form.data[i]).value)
			// 	    }
			// 	}
			// }
		},
		checkError(){
			return(true)
		}
	},
	mounted() {
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
				this.setStripeProp({prop: 'ach_public_token', value: public_token})
				this.setStripeProp({prop: 'ach_account_id', value: metadata.account_id})
				this.plaidSendCredentials()

				var extraDetails = {
				
				};

				var errors = null

				let bankcustomername = document.getElementById("bankcustomername").value
				extraDetails['bankcustomername'] = bankcustomername

				console.log("errors: bankcustomername", bankcustomername)

				errors = ValidateFormStep(self.form.data[1], bankcustomername)
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
		
		var stripe = Stripe('pk_test_jW4CJTGamhoH2cCxQljIKiwd');
		var elements = stripe.elements();
		var card = elements.create('card', {
			style: {
				base: {
					iconColor: '#eca661',
					color: '#ffffff',
					lineHeight: '40px',
					fontWeight: 300,
					fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
					fontSize: '15px',

					'::placeholder': {
						color: '#CFD7E0',
					},
				},
			}
		});
		card.mount('#card-element');
		var self = this;
		function setOutcome(result) {
			var errorElement = document.querySelector('.error');
			errorElement.classList.remove('visible');

			var error = false

			if (result.token) {
				// Use the token to create a charge or a customer
				// https://stripe.com/docs/charges
				self.setPaymentToken(result.token.id);
				self.setStripeProp({prop: 'cc_payment_token', value: result.token.id})

			} else if (result.error) {
				errorElement.textContent = result.error.message;
				errorElement.classList.add('visible');
				error = true
			}
			return(error)
		}
		card.on('change', function(event) {
			self.cardError = setOutcome(event);
			console.log(self.cardError)
		});
		document.querySelector('#btn_review').addEventListener('click', function(e) {
			//e.preventDefault();

			var extraDetails = {
				
			};

			var script = "submitpayment"

			var noFormErrors = true

			let errors = null

			if(self.payment_type == 'card'){
				
				let cardName = document.getElementById("cardname").value
				extraDetails['name'] = cardName

				errors = ValidateFormStep(self.form.data[0], cardName)
				if (errors["valid"] == false)
				{
					forEachValue(errors["errors"], (value, key) => {
						value.map((val) => {
							self.setError({key: key, value: value})
						})
					})

					noFormErrors = false
				}

				if(noFormErrors){
					stripe.createToken(card, extraDetails).then(setOutcome).then(() => {
						if(!self.cardError){
							self.buttonAction(null, script)	
						}
					});
				}
			}
			else if(self.payment_type == 'ach'){

				let bankcustomername = document.getElementById("bankcustomername").value
				extraDetails['bankcustomername'] = bankcustomername

				console.log("error bankcustomername:", bankcustomername)

				errors = ValidateFormStep(self.form.data[1], bankcustomername)
				if (errors["valid"] == false)
				{
					forEachValue(errors["errors"], (value, key) => {
						value.map((val) => {
							self.setError({key: key, value: value})
						})
					})

					noFormErrors = false
				}

				if(self.getAchPaymentToken == ""){
					let accountNumber = document.getElementById("accountnumber").value
					extraDetails['accountNumber'] = accountNumber

					errors = ValidateFormStep(self.form.data[2], accountNumber)
					if (errors["valid"] == false)
					{
						forEachValue(errors["errors"], (value, key) => {
							value.map((val) => {
								self.setError({key: key, value: value})
							})
						})

						noFormErrors = false
					}

					let routingNumber = document.getElementById("routingnumber").value
					extraDetails['routingNumber'] = routingNumber

					errors = ValidateFormStep(self.form.data[3], routingNumber)
					if (errors["valid"] == false)
					{
						forEachValue(errors["errors"], (value, key) => {
							value.map((val) => {
								self.setError({key: key, value: value})
							})
						})

						noFormErrors = false
					}

					script = "submitach"

					if(noFormErrors){
						self.buttonAction(null, "submitach")
					}
				}
				else{
					if(noFormErrors){
						self.buttonAction(null, script)	
					}
				}
			}
			else if(self.payment_type == 'verify'){

				let verify1 = document.getElementById("verify1").value
				extraDetails['verify1'] = verify1

				errors = ValidateFormStep(self.form.data[4], verify1)
				if (errors["valid"] == false)
				{
					forEachValue(errors["errors"], (value, key) => {
						value.map((val) => {
							self.setError({key: key, value: value})
						})
					})

					noFormErrors = false
				}

				let verify2 = document.getElementById("verify2").value
				extraDetails['verify2'] = verify2

				errors = ValidateFormStep(self.form.data[5], verify2)
				if (errors["valid"] == false)
				{
					forEachValue(errors["errors"], (value, key) => {
						value.map((val) => {
							self.setError({key: key, value: value})
						})
					})

					noFormErrors = false
				}

				script = "verifyach"

				if(noFormErrors){
					self.buttonAction(null, script)
				}
			}

			

		});
	},
	computed: {
		...mapGetters([
			'getErrors',
			'getAchPaymentToken',
			'getCurrentFormStep',
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

.btn-plaid-success {
	padding: 10px 20px;
	color: white!important;
	cursor: initial!important;
	background: #5cb85c!important;
	border: 1px solid #00a25c;
	transition: 0.2s background, 0.2s color;

	&:hover {
		padding: 10px 20px;
		color: white!important;
		cursor: initial!important;
		border-color: #00a25c!important;
		background: #5cb85c!important;
		// border: 1px solid #FFFFFF;
	}
	&:focus {
		color: white!important;
		cursor: initial!important;
	}
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
	color: white;
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
	color: white;
}

.nav-tabs li a:active, .nav-tabs li a:visited {
	color: white;
}

</style>