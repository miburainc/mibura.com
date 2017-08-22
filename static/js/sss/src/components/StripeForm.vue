<template>
	<div>
		<div id="card-element" class="field"></div>
		<div class="outcome">
			<div class="error" role="alert"></div>
			<!--
			<div class="success">
			Success! Your Stripe token is <span class="token"></span>
			</div>
			-->
		</div>
		<div>
			<button id='linkButton' class="btn btn-link">Click here to pay by ACH</button>
		</div>
	</div>
</template>

<script>

import {mapActions} from 'vuex'

export default {
	props: [''],
	methods: {
		...mapActions([
			'setPaymentToken',
			'setStripeProp'
		])
	},
	mounted() {
		var linkHandler = Plaid.create({
			env: 'sandbox',
			clientName: 'Stripe/Plaid Test',
			key: '0e355574b026a7c38406d02a00bc4d',
			product: ['auth'],
			selectAccount: true,
			onSuccess: function(public_token, metadata) {
				// Send the public_token and account ID to your app server.
				console.log('public_token: ' + public_token);
				console.log('account ID: ' + metadata.account_id);
				this.setStripeProp({prop: 'ach_public_token', value: public_token})
				this.setStripeProp({prop: 'ach_account_id', value: metadata.account_id})
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

<style scoped>

#linkButton {
	margin-top: 10px;
	padding-top: 0px;
}

</style>