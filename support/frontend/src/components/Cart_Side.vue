<template>

<div id="side_cart">
	<div :style="cartHeaderStyle">
		<div class="text-center" style="padding: 10px;">
			<h2 class="cart-tray" :style="textColorPlan">${{ numWithCommas(getGrandTotal) }}</h2>
		</div>
		<div>
			<div class="text-center">
				<button 
					type="button" 
					class="btn-plan" 
					v-for="(p, index) in getPlans" 
					:value="p.code"
					@click="setPlan"
					:style="{
						color: p.color == '#000000' ? 'white' : 'black',
						backgroundColor: p.color,
						fontSize: '11px'
					}"
				>
					{{p.name}}
				</button>
			</div>
			
		</div>

	</div>

	<div style="color: black;">
		<h4 class="text-center">Cart</h4>
		<table id="cart-table-header" class="table table-condensed table-striped">
			<thead>
				<th :style="cartHeaderStyle">Product</th>
				<th class="text-right" :style="cartHeaderStyle">Subtotal</th>
				<th class="text-right" :style="cartHeaderStyle">Options</th>
			</thead>
		</table>
		<div style="max-height:150px;overflow:auto;margin-bottom:10px;">
			<table class="table table-striped table-condensed table-hover">
				<tbody class="cart-table-body">
					<tr v-if="this.cart.length < 1" class="text-center">
						<td colspan="4">None</td>
					</tr>
					<tr v-else v-for="(item, index) in cart">
						<td>
							<i v-if="item.type=='cloud'" class="fa fa-cloud" aria-hidden="true"></i>
							{{item.brand}} {{item.model}}
						</td>
						<td class="text-center">
							${{ numWithCommas(getProductSubtotal(index)-getProductSubtotal(index)*getCurrentDiscount) }}
						</td>
						<td class="text-right">
							<div class="btn-group">
								<button v-if="item.type != 'cloud'" type="button" class="btn btn-xs btn-warning" @click="editItem(item.sku, index)"><i class="fa fa-pencil" aria-hidden="true"></i></button>&nbsp;
								<button type="button" class="btn btn-xs btn-danger" @click="removeItem(item.id, index)"><i class="fa fa-times" aria-hidden="true"></i></button>
							</div>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
		<div class="btn-group btn-4">
			<button type="button" class="btn btn-sm btn-success" @click="buttonStartNewItem"><i class="fa fa-plus" aria-hidden="true"></i> Item</button>
			<button type="button" class="btn btn-sm btn-info" @click="buttonStartCloud"><i class="fa fa-cloud" aria-hidden="true"></i> Cloud</button>
			<button type="button" class="btn btn-sm btn-primary" @click="buttonGetEstimate"><i class="fa fa-upload" aria-hidden="true"></i> Quote</button>
			<button type="button" class="btn btn-sm btn-danger" @click="clear_cart"><i class="fa fa-times" aria-hidden="true"></i> Clear</button>
		</div>
		<br><br>
		<div class="btn-group btn-2">
			<button type="button" class="btn btn-sm btn-info" @click="buttonPhoneSupport">
				<i class="fa fa-phone" aria-hidden="true"></i>
				&nbsp;Call Sales
			</button>
			<button type="button" class="btn btn-sm btn-primary" @click="buttonGetPDF">
				<i class="fa fa-file-pdf-o" aria-hidden="true"></i>
				&nbsp;Get Quote
			</button>
		</div>
			
		<div v-if="get_cart_reference">
			<h4>Cart Reference Code: {{get_cart_reference}}</h4>
		</div>
		<div v-if="Object.keys(getClientInfo).length > 0" class="pad-10">
			<div class="col-xs-6">
				{{getClientInfo['first_name']}} {{getClientInfo['last_name'] }}<br>
				{{getClientInfo['email']}}<br>
				{{getClientInfo['company']}}<br>
				{{getClientInfo['phone']}}
			</div>
			<div class="col-xs-6">
				{{getClientInfo['street']}},
				{{getClientInfo['street2']}}<br>
				{{getClientInfo['city']}}, {{getClientInfo['state']}}<br>
				{{getClientInfo['zipcode']}}, {{getClientInfo['country']}}<br>
			</div>
			<button type="button" class="btn btn-xs btn-link" @click="buttonEditClient">Edit</button>
		</div>
		<div v-else class="pad-10 text-center">
			<button type="button" class="btn btn-default" @click="buttonStartClientInfo">Enter your information</button>
		</div>
		
		<div>
			<div class="form-group">
				<h4 style="color: black; text-align: center; padding: 10px;">{{writeOutSupportLength}}</h4>
				<div class="btn-group btn-2">
					<button class="btn btn-sm btn-danger" @click="setSupportYears(getSupportMonths - 6)"><i class="fa fa-minus" aria-hidden="true"></i></button>
					<button class="btn btn-sm btn-success" @click="setSupportYears(getSupportMonths + 6)"><i class="fa fa-plus" aria-hidden="true"></i></button>
				</div>
				<input style="color: black;" class="form-control" type="hidden" min="0.5" max="9" step="0.5" name="years" @change="setSupportYears" :value="getSupportMonths/12">
			</div>
		</div>

		<div class="pad-10">
			<div class="text-right pad-10">
				SubTotal: ${{ numWithCommas(getTotal) }}<br>
				%{{getCurrentDiscount*100}} Discount: &nbsp;
				- ${{numWithCommas(getTotal*getCurrentDiscount)}}<br>
				<span style="font-size: 1.2em;font-weight:700;">Estimate Total: ${{ numWithCommas(getGrandTotal) }}</span>
			</div>
			<div class="btn-group btn-2">
				<button type="button" class="btn btn-sm btn-default" data-toggle="modal" data-target="#termsModal">
					Terms &amp; Conditions
				</button>
				<button type="button" class="btn btn-sm btn-success" @click="formPurchase">
					<i class="fa fa-check" aria-hidden="true"></i>
					&nbsp;Purchase
				</button>
			</div>
		</div>
	</div>
</div>

</template>

<script>

import axios from 'axios'

import { mapGetters, mapActions } from 'vuex'

import {URL_ROOT,API_ROOT,step_names} from '../store/values'

import moment from 'moment'
import velocity from 'velocity-animate'

export default {
	data () {
		return {
			
		}
	},
	created() {
		
	},
	methods: {
		...mapActions([
			'editCartItem',
			'removeCartItem',
			'setSupportMonths',
			'setSupportYears',
			'clearCart',
			'setCurrentFormStep',
			'saveCart',
			'setCurrentPlan',
			'checkout',
			'serverSetClient',
			'serverGetEstimatePdf',
			'setEstimatePdfFile',
			'setAcceptedTerms',
			'addNotification',
		]),

		setPlan(el) {
			let val = el.target.value
			switch(val) {
				case 'silver':
					this.addNotification({
						type: 'success',
						message: 'Pro Silver provides 4 hour response for the lowest price! <a href="/support#plan-comparison" target="_blank">Click here to see more!</a>'
					})
					break;
				case 'gold':
					this.addNotification({
						type: 'success',
						message: 'Pure Gold provides 15 min response and free cloud support! <a href="/support#plan-comparison" target="_blank">Click here to see more!</a>'
					})
					break;
				case 'black':
					this.addNotification({
						type: 'success',
						message: 'Carbon Black provides 15 min response and a dedicated security & compliance team! <a href="/support#plan-comparison" target="_blank">Click here to see more!</a>'
					})
					break;
			}
			this.setCurrentPlan(val)
		},
		formPurchase() {
			if (this.cart.length < 1) {
				this.addNotification({
					type: 'warning',
					message: 'Please add items to your cart before clicking purchase!'
				})
				this.buttonStartNewItem()
			}
			else if (Object.keys(this.getClientInfo) < 10) {
				this.addNotification({
					type: 'warning',
					message: 'Please fill out your information!'
				})
				this.buttonStartClientInfo()
			}
			else if (!this.get_payment_token) {
				this.addNotification({
					type: 'warning',
					message: 'Please fill out your payment information!'
				})
				this.buttonStartPayment()
			}
			else if (!this.get_accepted_terms) {
				$('#termsModal').modal('show')
			}
			else {
				this.serverSetClient().then(() => {
					this.saveCart().then(() => {
						this.checkout()
							.then((status) => {
								console.log("after purchase callback")
								console.log(status)
								if (status == false) {
									// Failed
									this.addNotification({
										message: "Unverified items in cart.  Please call Mibura to get your cart approved for purchase.",
										type: "danger"
									})
									this.addNotification({
										message: "To speak with Mibura about your support plan, click 'Call Sales' to speak with a Mibura sales representative.",
										type: "warning"
									})
									this.addNotification({
										message: "To revisit later, click the 'Get Quote' button in your cart to print, download, or be emailed your PDF Estimate.",
										type: "info"
									})
								}
							})
					})
				})
				
			}
		},
		buttonStartPayment() {
			velocity(document.body, "scroll", { duration: 1000, mobileHA: false, offset: 0 });
			this.setCurrentFormStep(step_names.payment)
		},
		buttonStartCloud() {
			velocity(document.body, "scroll", { duration: 1000, mobileHA: false, offset: 0 });
			this.setCurrentFormStep(step_names.cloud)
		},
		buttonEditClient() {
			velocity(document.body, "scroll", { duration: 1000, mobileHA: false, offset: 0 });
			this.setCurrentFormStep(step_names.client_info)
		},
		buttonStartNewItem() {
			velocity(document.body, "scroll", { duration: 1000, mobileHA: false, offset: 0 });
			this.setCurrentFormStep(step_names.brand)
		},
		buttonStartClientInfo() {
			velocity(document.body, "scroll", { duration: 1000, mobileHA: false, offset: 0 });
			this.setCurrentFormStep(step_names.client_info)
		},
		buttonPhoneSupport() {
			if (Object.keys(this.getClientInfo).length<1) {
				this.addNotification({
					type: 'warning',
					message: 'Please provide your contact information.'
				})
				this.buttonStartClientInfo()
			}
			else {
				this.serverSetClient().then(() => {
					this.saveCart()
					$('#chatModal').modal('show')
				})
				
			}
		},
		buttonGetEstimate() {
			$('#estimateIdModal').modal('show')
		},
		buttonGetPDF() {
			if (this.cart.length < 1) {
				this.addNotification({
					type: 'warning',
					message: 'Please add items to your cart!'
				})
				this.buttonStartNewItem()
			}
			else if (Object.keys(this.getClientInfo).length<1) {
				this.addNotification({
					type: 'warning',
					message: 'Please provide your contact information.'
				})
				this.buttonStartClientInfo()
			}
			else {
				// Reset pdf to nothing
				this.setEstimatePdfFile(null);
				// Send request for new pdf file
				this.saveCart(this.getClientInfo)
					.then(() => {
						this.serverGetEstimatePdf()
					})
				$('#pdfModal').modal('show')
			}
		},
		clear_cart() {
			if (confirm("Are you sure you want to clear your cart?") == true) {
				this.clearCart()
			}
		},

		numWithCommas(x) {
			let num = x.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
			return num
		},
		
		editItem(id, index) {
			this.editCartItem({
				id: id,
				index: index
			});
			velocity(document.body, "scroll", { duration: 1000, mobileHA: false, offset: 0 });
		},
		removeItem(id, index) {
			this.removeCartItem({
				id: id,
				index: index
			})
		},
	},
	computed: {
		...mapGetters({
			cart: 'getCart',
			getPlans: 'getPlans',
			getPlan: 'getPlan',
			getSupportMonths: 'getSupportMonths',
			getMultiplier: 'getMultiplier',
			getClientInfo: 'getClientInfo',
			get_payment_token: 'getPaymentToken',
			get_cart_reference: 'getCartReference',
			get_accepted_terms: 'getAcceptedTerms',
			current_plan: 'getCurrentPlan',
			getTotal: 'getTotal',
			getProductSubtotal: 'getProductSubtotal',
			getGrandTotal: 'getGrandTotal',
			getCurrentDiscount: 'getCurrentDiscount',
			get_discounts: 'getDiscounts',
		}),

		textColorPlan() {
			return {'color': this.current_plan == 'black' ? 'white' : 'black' }
		},
		
		cartHeaderStyle() {
			let plan = this.getPlan(this.current_plan)
			return {
				'padding-top': '10px',
				'background-color': plan.color, 
				'color': this.current_plan == 'black' ? 'white' : 'black'
			}
		},
		writeOutSupportLength() {
			let str = ""
			let lenArray = String(this.getSupportMonths/12).split('.')
			if (lenArray.length > 1) {
				if(lenArray[0] == 1){
					str = lenArray[0] + " Year & 6 months"	
				}
				else if(lenArray[0] != 0){
					str = lenArray[0] + " Years & 6 months"		
				}
				else{
					str = "6 months"
				}
			}
			else {
				if(lenArray[0] == 1){
					str = lenArray[0] + " Year"	
				}
				else if(lenArray[0] != 0){
					str = lenArray[0] + " Years"
				}
			}
			return str
		}
	}
}

</script>

<style lang="scss" scoped>

#side_cart {
	// margin-top: 15%;
	border-radius: 5px;
	border: 0px solid #444444;
	background-color: white;
}

#cart-table-header {
	margin-bottom: 0;
}

.cart-table-body tr td {
	font-size: 1.1em;
}

.btn-2, .btn-4 {
	width: 100%;
}

.btn-4 .btn {
	width: 25%;
} 

.btn-2 .btn {
	width: 50%!important;
}

.btn-plan {
	width: 33.33%;
	padding: 10px;
	border: 0;
}

.btn-plan:focus {
    outline: 0;
}

.cart-tray {
	color: #000000;
}

h1, h2, h3, h4, table, thead, tbody, span, div, p, form {
	color: #000000;
}

h2 {
	font-weight: 300;
	font-size: 2.5em
}

h1, h2, h3, h4 {
	margin: 0;
}


</style>