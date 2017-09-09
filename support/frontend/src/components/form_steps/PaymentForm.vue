<template>
	<div id="stripe-payment-form">
		<ul class="nav nav-tabs">
			<li role="presentation" :class="{active: payment_type=='card'}"><a style="cursor: pointer;" @click="switchTabs('card')">Credit Card</a></li>
			<li role="presentation" :class="{active: payment_type=='ach'}"><a style="cursor: pointer;" @click="switchTabs('ach')">Bank ACH</a></li>
		</ul>
		<div class="payment-box">

			<div v-show="payment_type=='card'" class="stripe-form-cc pad-10">

				<form-text-input :step="form.data[0]" id="cardName"></form-text-input>
				<form-text-input :step="form.data[1]" id="cardPhone"></form-text-input>

				<label>Card Info</label>
				<div id="card-element" class="field"></div>
				<div class="outcome">
					<div class="error" role="alert"></div>
					<!--
					<div class="success"> 
					Success! Your Stripe token is <span class="token"></span>
					</div>
					-->
				</div>
			</div>
			
			<div v-show="payment_type=='ach'" class="stripe-form-ach pad-10" style="margin-bottom:5px;">

				<form-text-input :step="form.data[2]" id="bankName"></form-text-input>
				<form-text-input :step="form.data[3]" id="bankPhone"></form-text-input>
				
				<div class="container-fluid" style="border-top: 1px solid #8493A8; padding-top:15px; margin-top:10px;">
					<div class="row">
						<div class="col-sm-5" style=" text-align:center;">
							<button style="margin: 30px 0px 0px 18%; padding: 30px" v-on:keypress.enter.prevent type="button" v-show="payment_type=='ach'" id='linkButton' class="btn btn-lg btn-outline-info payment-button">Login to <br> bank account</button>
						</div>
						<div class="col-sm-2 text-center">
							<div class="line"></div>
							<div class="orText">or</div>
							<div class="line"></div>
						</div>
						<div class="col-sm-5">
							<form-text-input  id="accountNumber" style="margin-top:17px":step="form.data[4]"></form-text-input>
							<form-text-input  id="routingNumber" :step="form.data[5]"></form-text-input>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div v-bind:style="form.buttonStyle" class="btn-2-round" > 	

			<button v-on:keypress.enter.prevent :class="form.buttons[0].class" type="button"
			@click="(el) => {buttonAction(el, form.buttons[0].script)}">{{form.buttons[0].label}}</button><button v-on:keypress.enter.prevent :class="form.buttons[1].class" type="button" @click="completePayment">{{form.buttons[1].label}}</button>
			
		</div>
	</div>
</template>

<script>

import {mapActions} from 'vuex'
import FormTextInput from '../FormTextInput.vue'
import {ValidateFormStep} from '../../scripts/functions.js'

export default {
	components: {
		'form-text-input': FormTextInput
	},
	data() {
		return {
			payment_type: 'card',
		}
	},
	props: ['form', 'buttonAction'],
	methods: {
		...mapActions([
			'setPaymentToken',
			'setStripeProp',
			'plaidSendCredentials',
			'clearErrors'
		]),
		sendplaidcredentials() {
			this.plaidSendCredentials()
		},
		switchTabs(newTab){
			this.payment_type = newTab
		},
		completePayment(){

			if(this.payment_type == 'card'){
				let cardName = document.getElementById("cardname").value
				//error = ValidateFormStep(this.form[0], cardName)
				console.log(cardName)
				//console.log(error)
				let cardPhone = document.getElementById("cardphone").value
				//error = ValidateFormStep(this.form[1], cardPhone)
				console.log(cardPhone)
				//console.log(error)
			}
			else if(this.payment_type == 'ach'){
				let bankName = document.getElementById("bankname").value
				let bankPhone = document.getElementById("bankphone").value
				let accountNumber = document.getElementById("accountnumber").value
				let routingNumber = document.getElementById("routingnumber").value
				console.log(bankName)
				console.log(bankPhone)
				console.log(accountNumber)
				console.log(routingNumber)
			}
			
			

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
			if (result.token) {
				// Use the token to create a charge or a customer
				// https://stripe.com/docs/charges
				self.setPaymentToken(result.token.id);
				self.setStripeProp({prop: 'cc_payment_token', value: result.token.id})
			} else if (result.error) {
				errorElement.textContent = result.error.message;
				errorElement.classList.add('visible');
			}
		}
		card.on('change', function(event) {
			setOutcome(event);
		});
		document.querySelector('#btn_review').addEventListener('click', function(e) {
			e.preventDefault();
			var form = document.querySelector('form');
			var extraDetails = {
				name: form.querySelector('input[name=cardholder-name]').value,
			};
			stripe.createToken(card, extraDetails).then(setOutcome);
		});
	}
}

</script>

<style lang="scss" scoped>

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