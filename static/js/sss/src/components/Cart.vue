<template>

<div id="sss-cart" :style="cartStyle">
	<div class="row" :style="cartHeaderStyle">
		<div class="col-xs-6 col-md-4">
			<h2 class="cart-tray" :style="textColorPlan">${{ numWithCommas(getGrandTotal) }}</h2>
		</div>
		<div class="col-md-4">
			<div class="text-center" :style="textColorPlan">Plan
			<div class="form-group">
				<select class="form-control" :value="current_plan" @change="setPlan" :style="textColorPlan">
					<option v-for="(p, index) in plans" :value="p.code">{{p.name}}</option>
				</select>
			</div>
			</div>
			
		</div>
		<div class="col-xs-6 col-md-4">
			<h2 class="cart-tray text-right"><a :style="[textColorPlan, {'cursor': 'pointer'}]" @click="scrollDown">View Cart</a></h2>
		</div>
	</div>
	<div class="container">
	<div class="row">
		<div class="col-xs-12" style="color: black; padding: 15px;">
			<h1 class="text-center">Cart</h1>
			<table class="table table-condensed table-striped">
				<thead>
					<th :style="cartHeaderStyle">Product</th>
					<th class="text-center" :style="cartHeaderStyle">Subtotal</th>
					<th v-if="getCurrentDiscount" class="text-center" :style="cartHeaderStyle">Discount Price</th>
					<th class="text-right" :style="cartHeaderStyle">Options</th>
				</thead>
				<tbody>
					<tr v-if="this.cart.length < 1" class="text-center">
						<td colspan="4">None</td>
					</tr>
					<tr v-else v-for="(item, index) in cart">
						<td>
							<i v-if="item.type=='cloud'" class="fa fa-cloud" aria-hidden="true"></i>
							{{item.brand}} {{item.model}}
						</td>
						<td class="text-center">
							${{ numWithCommas(getProductSubtotal(index)) }}
						</td>
						<td v-if="getCurrentDiscount" class="text-center">
							${{ numWithCommas(getProductSubtotal(index)-getProductSubtotal(index)*getCurrentDiscount) }}
						</td>
						<td class="text-right">
							<div class="btn-group">
								<button v-if="item.type != 'cloud'" type="button" class="btn btn-sm btn-warning" @click="editItem(item.sku, index)"><i class="fa fa-pencil" aria-hidden="true"></i> Edit</button>&nbsp;
								<button type="button" class="btn btn-sm btn-danger" @click="removeItem(item.id, index)"><i class="fa fa-times" aria-hidden="true"></i> Remove</button>
							</div>
						</td>
					</tr>
				</tbody>
			</table>
			<div class="btn-group">
				<button type="button" class="btn btn-success" @click="buttonStartNewItem"><i class="fa fa-plus" aria-hidden="true"></i> Add Item</button>
				<button type="button" class="btn btn-info" @click="buttonStartCloud"><i class="fa fa-cloud" aria-hidden="true"></i> Add Cloud Provider</button>
				<button type="button" class="btn btn-primary" @click="buttonGetEstimate"><i class="fa fa-upload" aria-hidden="true"></i> Input Quote ID</button>
				<button type="button" class="btn btn-danger" @click="clear_cart"><i class="fa fa-times" aria-hidden="true"></i> Clear Cart</button>
			</div>
				
			<hr><br>
			<div class="pull-right">
				<h4>Cart Reference Code: {{get_cart_reference}}</h4>
				<button type="button" class="btn btn-default" data-toggle="modal" data-target="#termsModal">
					View Terms and Conditions
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
			
			<div style="color: black; width: 50%; margin: 0 auto;">
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
							&nbsp;Speak with Sales
						</button>
						<button type="button" class="btn btn-primary" @click="buttonGetPDF">
							<i class="fa fa-cart-arrow-down" aria-hidden="true"></i>
							&nbsp;Get Quote
						</button>
						<button type="button" class="btn btn-success" @click="formPurchase">
							<i class="fa fa-check" aria-hidden="true"></i>
							&nbsp;Purchase Support
						</button>
					</div>
				</div>
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
			current_plan2: "silver",
			discounts: [],
			current_discount: 0.0,
		}
	},
	created() {
		axios.get(API_ROOT+'discounts')
			.then((response) => {
				console.log(response)
				this.discounts = response.data.results
			})
			.catch((error) => {
				console.error(error)
			})
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
		]),
		setPlan(el) {
			let val = el.target.value
			this.setCurrentPlan(val)
		},
		formPurchase() {
			if (this.cart.length < 1) {
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
				this.serverSetClient().then(() => {
					this.saveCart().then(() => {
						this.checkout()
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
			if (this.cart.length < 1) {
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
			if (this.cart.length < 1) {
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
		// 
		// Product Pricing //
		// 
		getProductAge(product) {
			let product_release = moment(product.release)
			let today = moment()
			let age_months = today.diff(product_release, 'months')
			let age = age_months / 6
			return Math.round(age)
		},
		getProductPrice(cart_index) {
			// 
			// Calculate product price depending on plan selected by customer
			// 
			let cost = 0
			let product = this.cart[cart_index]
			let plan_name = ''
			switch(this.current_plan) {
				case 'silver':
					// Silver
					plan_name = 'silver'
					break;
				case 'gold':
					// Gold
					plan_name = 'gold'
					break;
				case 'black':
					// Black
					plan_name = 'black'
					break;
			}
			// Product multiplier per plan e.g 1.0x
			let pp = product['price_'+plan_name]
			// Product Category multiplier e.g 1.2x
			let pm = product.category.price_multiplier
			// Plan base product price e.g $49/yr
			let pc = this.getPlans(this.current_plan).cost
			// Calculation and then divided by half since plans are sold in 6 month increments
			cost = (pp * pm * pc) / 2
			return cost
		},
		getProductSubtotal(cart_index) {
			//
			// Get product line item price
			//
			let product = this.cart[cart_index]
			let product_price = this.getProductPrice(cart_index)
			let product_age = this.getProductAge(product)
			// price_iterations - how many half year increments to add
			let price_iterations = this.getSupportMonths/6
			// inc - amount to add to base price based on product age
			let inc = product.category.yearly_tax
			
			let price = 0.0
			// Calculate price base price depending on age
			for (let e=0; e<product_age; e++) {
				price += (product_price * inc)
			}

			// Calculate price into future for length of support bought by client
			for (let i=0; i<price_iterations; i++) {
				price += product_price + (product_price * inc)
			}

			return price
		},
		getPlans(plan) { 
			for (let i=0; i<this.plans.length; i++) {
				if (this.plans[i].code == plan) {
					return this.plans[i]
				}
			}
			return false
		},
	},
	computed: {
		...mapGetters({
			cart: 'getCart',
			plans: 'getPlans',
			getSupportMonths: 'getSupportMonths',
			getMultiplier: 'getMultiplier',
			getClientInfo: 'getClientInfo',
			get_payment_token: 'getPaymentToken',
			get_cart_reference: 'getCartReference',
			get_accepted_terms: 'getAcceptedTerms',
			current_plan: 'getCurrentPlan',
		}),
		getCurrentDiscount() {
			let d = 0.0
			for (let i=0; i<this.discounts.length; i++) {
				if (this.getSupportMonths/12 >= this.discounts[i].year_threshold) {
					if (this.discounts[i].discount_percent > d) {
						d = this.discounts[i].discount_percent
					}
				}
			}
			return d
		},
		getTotal() {
			let total = 0;
			for (let i=0; i<this.cart.length; i++) {
				total += this.getProductSubtotal(i)
			}
			
			return total
		},
		getGrandTotal() {
			let total = this.getTotal
			let final = total - (total * this.getCurrentDiscount)
			return final
		},
		textColorPlan() {
			return {'color': this.current_plan == 'black' ? 'white' : 'black' }
		},
		cartStyle() {

		},
		
		cartHeaderStyle() {
			let plan = this.getPlans(this.current_plan)
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


</style>