<template>

<div id="sss-cart" :style="cartStyle">
	<div id="cart-header" class="row no-pad" :style="cartHeaderStyle">
		<div class="col-xs-12">
			<div class="cart-tray" :style="textColorPlan">${{ numWithCommas(getGrandTotal) }}
			<a :style="[textColorPlan, {'cursor': 'pointer', 'float': 'right'}]" @click="scrollDown">View Cart</a></div>
		</div>
		<div class="col-xs-12 no-pad">
			<div class="no-pad" :style="textColorPlan">
					<button class="btn-plan" v-for="(p, index) in get_plans" @click="setPlan" :style="{'color': p.color == '#000000' ? 'white' : 'black', backgroundColor: p.color}" :value="p.code">
						{{p.name}}
					</button>
			</div>
			
		</div>
	</div>
	<div id="cart-body" class="col-xs-12" style="color: black;">
		<h1 class="text-center">Cart</h1>
		<table class="table table-condensed table-striped">
			<thead>
				<th :style="cartHeaderStyle">Product</th>
				<th class="text-center" :style="cartHeaderStyle">Subtotal</th>
				<th class="text-right" :style="cartHeaderStyle">Options</th>
			</thead>
			<tbody>
				<tr v-if="this.get_cart.length < 1" class="text-center">
					<td colspan="4">None</td>
				</tr>
				<tr v-else v-for="(item, index) in get_cart">
					<td>
						<i v-if="item.type=='cloud'" class="fa fa-cloud" aria-hidden="true"></i>
						{{item.brand}} {{item.model}}
					</td>
					<td class="text-center">
						${{ numWithCommas(getProductSubtotal(index)-getProductSubtotal(index)*getCurrentDiscount) }}
					</td>

					<td class="text-right">
						<div class="btn-group">
							<button v-if="item.type != 'cloud'" type="button" class="btn btn-sm btn-warning" @click="editItem(item.sku, index)"><i class="fa fa-pencil" aria-hidden="true"></i></button>&nbsp;
							<button type="button" class="btn btn-sm btn-danger" @click="removeItem(item.id, index)"><i class="fa fa-times" aria-hidden="true"></i></button>
						</div>
					</td>
				</tr>
			</tbody>
		</table>
		<div class="btn-group">
			<button type="button" class="btn btn-sm btn-success" @click="buttonStartNewItem"><i class="fa fa-plus" aria-hidden="true"></i> Item</button>
			<button type="button" class="btn btn-sm btn-info" @click="buttonStartCloud"><i class="fa fa-cloud" aria-hidden="true"></i> Add Cloud</button>
			<button type="button" class="btn btn-sm btn-primary" @click="buttonGetEstimate"><i class="fa fa-upload" aria-hidden="true"></i> Open Quote</button>
			<button type="button" class="btn btn-sm btn-danger" @click="clear_cart"><i class="fa fa-times" aria-hidden="true"></i> Clear Cart</button>
		</div>
			
		<hr><br>
		<div class="pull-right">
			<h4>Cart Reference Code: {{get_cart_reference}}</h4>
			<button type="button" class="btn btn-default" data-toggle="modal" data-target="#termsModal">
				Terms &amp; Conditions
			</button>
		</div>
		<div>
			<h4>Your information:</h4>
			<div v-if="Object.keys(getClientInfo).length > 0">
				<div v-for="key in Object.keys(getClientInfo)">{{key}}: {{getClientInfo[key]}}
				</div>
				<br>
				<button type="button" class="btn btn-link" @click="buttonEditClient">Edit</button>
			</div>
			<div v-else>
				<button type="button" class="btn btn-default" @click="buttonStartClientInfo">Enter your information</button>
			</div>
		</div>
		
		<div>
			<div class="form-group">
				<!-- <label style="color: black;">Months</label>
				<input style="color: black;" class="form-control" type="number" min="6" max="108" name="years" step="6" @change="setSupportMonths" :value="getSupportMonths"> -->
				<label style="color: black;">{{writeOutSupportLength}}</label>
				<input style="color: black;" class="form-control" type="number" min="0.5" max="9" step="0.5" name="years" @change="setSupportYears" :value="getSupportMonths/12">
			</div>
			<div style="color: black;" class="text-right">
				SubTotal: ${{ numWithCommas(getTotal) }}<br>
				%{{getCurrentDiscount*100}} Discount: &nbsp;
				- ${{numWithCommas(getTotal*getCurrentDiscount)}}<br>
				<strong>Estimate Total: ${{ numWithCommas(getGrandTotal) }}</strong>
				<br>
				<div class="btn-group">
					<button type="button" class="btn btn-info" @click="buttonPhoneSupport">
						<i class="fa fa-phone" aria-hidden="true"></i>
						&nbsp;Call Sales
					</button>
					<button type="button" class="btn btn-primary" @click="buttonGetPDF">
						<i class="fa fa-file-pdf-o" aria-hidden="true"></i>
						&nbsp;Get Quote
					</button>
					<button type="button" class="btn btn-success" @click="formPurchase">
						<i class="fa fa-check" aria-hidden="true"></i>
						&nbsp;Purchase
					</button>
				</div>
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
			this.setCurrentPlan(val)
		},
		formPurchase() {
			if (this.get_cart.length < 1) {
				this.buttonStartNewItem()
			}
			else if (Object.keys(this.getClientInfo) < 10) {
				this.buttonStartClientInfo()
			}
			else if (!this.get_payment_token) {
				this.buttonStartPayment()
			}
			else if (!this.get_accepted_terms) {
				$('#termsModal').modal('show')
			}
			else {
				console.log("Purchase -- ")
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
			console.log("buttonPhoneSupport")
			if (this.get_cart.length < 1) {
				this.buttonStartNewItem()
			}
			else if (Object.keys(this.getClientInfo).length<1) {
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
			console.log("buttonGetPDF")
			if (this.get_cart.length < 1) {
				this.buttonStartNewItem()
			}
			else if (Object.keys(this.getClientInfo).length<1) {
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
		scrollDown() {
			velocity(document.body, "scroll", { duration: 1000, mobileHA: false, offset: document.body.scrollHeight });
			// window.scrollTo(0,);
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
			numWithCommas: 'numWithCommas',
			get_cart: 'getCart',
			get_plans: 'getPlans',
			get_plan: 'getPlan',
			getSupportMonths: 'getSupportMonths',
			getMultiplier: 'getMultiplier',
			getClientInfo: 'getClientInfo',
			get_payment_token: 'getPaymentToken',
			get_cart_reference: 'getCartReference',
			get_accepted_terms: 'getAcceptedTerms',
			current_plan: 'getCurrentPlan',
			getCurrentDiscount: 'getCurrentDiscount',
			getProductSubtotal: 'getProductSubtotal',
			getTotal: 'getTotal',
			getGrandTotal: 'getGrandTotal',
			get_cart_changed: 'getCartChanged',
		}),
		textColorPlan() {
			return {'color': this.current_plan == 'black' ? 'white' : 'black' }
		},
		cartStyle() {

		},
		cartHeaderStyle() {
			let plan = this.get_plan(this.current_plan)
			return {
				'background-color': plan.color, 
				'color': this.current_plan == 'black' ? 'white' : 'black'
			}
		},
		writeOutSupportLength() {
			let str = ""
			let lenArray = String(this.getSupportMonths/12).split('.')
			if (lenArray.length > 1) {
				str = lenArray[0] + " Years & 6 months"
			}
			else {
				str = lenArray[0] + " Years"
			}
			return str
		}
	}
}

</script>

<style lang="scss" scoped>

#cart-header {
	position: fixed;
	left: 0;
	right: 0;
	bottom: 0;
	z-index: 1;
}

.no-pad {
	padding: 0;
}

.btn-plan:focus {
    outline: 0;
}

#cart-body {
	padding: 20px;
	padding-bottom: 100px;
}

#sss-cart {
	background: white;
}

.cart-tray {
	font-size: 1.4em;
}

h1, h2, h3, h4, table, thead, tbody, span, div, p, form {
	color: #000000;
}

h2 {
	font-weight: 300;
	font-size: 2.5em
}




</style>