<template>
	<div id="stripe-payment-form">
		<ul class="nav nav-tabs">
			<li role="presentation" :class="{active: payment_type=='card'}"><a href="#" @click="payment_type='card'">Credit Card</a></li>
			<li role="presentation" :class="{active: payment_type=='ach'}"><a href="#" @click="payment_type='ach'">Bank ACH</a></li>
		</ul>
		<div class="payment-box">

			<div v-show="payment_type=='card'" class="stripe-form-cc pad-10">
				<label>Name on Card</label>
				<input class="form-control" style="height: 45px;" type="text" name="cardholder-name"  placeholder="Name on card"/>
				<label>Cardholder Phone</label>
				<input class="form-control" style="height: 45px;" type="tel" name="ccphone"  placeholder="Cardholder Phone"/>
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
			
			<div v-show="payment_type=='ach'" class="stripe-form-ach pad-10">

				<label>Name on Bank Account</label>
				<input class="form-control" style="height: 45px;" type="text" name="cardholder-name"  placeholder="Name on card"/>
				<label>Phone on Bank Account</label>
				<input class="form-control" style="height: 45px;" type="tel" name="ccphone"  placeholder="Cardholder Phone"/>

				<div class="container-fluid">
					<div class="row">
						<div class="col-sm-6">
						<button type="button" v-show="payment_type=='ach'	" id='linkButton' class="btn btn-lg btn-success payment-button">Pay instantly with online bank account</button>
						</div>
						<div class="col-sm-6">
							<label>Bank</label>
							<input class="form-control" style="height: 45px;" type="text" name="bank-name"  placeholder="Bank"/>
							<label>Routing Number</label>
							<input class="form-control" style="height: 45px;" type="tel" name="routing-number"  placeholder="Routing Number"/>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div v-bind:style="form.buttonStyle"> 	
			<button type="button" v-for="btn in form.buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button>
			
		</div>
	</div>
</template>

<script>

import {mapActions} from 'vuex'

export default {
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
			'plaidSendCredentials'
		]),
		sendplaidcredentials() {
			this.plaidSendCredentials()
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