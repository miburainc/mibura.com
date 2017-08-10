<template>

<div id="sss-cart" :style="cartStyle">
	<div class="row" :style="cartHeaderStyle">
		<div class="col-xs-6 col-md-4">
			<h2 class="cart-tray" :style="textColorPlan">${{ getGrandTotal }}</h2>
		</div>
		<div class="col-md-4">
			<div class="text-center" :style="textColorPlan">Plan
			<div class="form-group">
				<select class="form-control" v-model="current_plan" @change="setCurrentPlan" :style="textColorPlan">
					<option v-for="(p, index) in plans" :value="index">{{p.name}}</option>
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
					<th>Product</th>
					<th class="text-center">Subtotal</th>
					<th class="text-right">Options</th>
				</thead>
				<tbody>
					<tr v-if="this.cart.length < 1" class="text-center">
						<td colspan="3">None</td>
					</tr>
					<tr v-else v-for="(item, index) in cart">
						<td>
							<i v-if="item.type=='cloud'" class="fa fa-cloud" aria-hidden="true"></i>
							{{item.brand}} {{item.model}}
						</td>
						<td class="text-center">
							${{ numWithCommas(getProductSubtotal(index)) }}
						</td>
						<td class="text-right">
							<div class="btn-group">
								<button type="button" class="btn btn-sm btn-warning" @click="editItem(item.sku, index)"><i class="fa fa-pencil" aria-hidden="true"></i> Edit</button>&nbsp;
								<button type="button" class="btn btn-sm btn-danger" @click="removeItem(item.id, index)"><i class="fa fa-times" aria-hidden="true"></i> Remove</button>
							</div>
						</td>
					</tr>
				</tbody>
			</table>
			<div class="btn-group">
				<button type="button" class="btn btn-success" @click="buttonStartNewItem"><i class="fa fa-plus" aria-hidden="true"></i> Add Item</button>
				<button type="button" class="btn btn-info" @click="buttonStartCloud"><i class="fa fa-cloud" aria-hidden="true"></i> Add Cloud Provider</button>
				<button type="button" class="btn btn-primary"><i class="fa fa-upload" aria-hidden="true"></i> Upload Quote</button>
				<button type="button" class="btn btn-danger" @click="clear_cart"><i class="fa fa-times" aria-hidden="true"></i> Clear Cart</button>
			</div>
				
			<hr><br>
			<div class="pull-right">
				<h4>Cart Reference Code: {{get_cart_reference}}</h4>
				<button type="button" class="btn btn-primary btn-lg" data-toggle="modal" data-target="#myModal">
					Launch demo modal
				</button>
			</div>
			<div>
				<h4>Your information:</h4>
				<div v-if="Object.keys(getClientInfo).length > 0">
					<div v-for="key in Object.keys(getClientInfo)">{{key}}: {{getClientInfo[key]}}
					</div>
					<br>
					<button type="button" class="btn btn-link">Edit</button>
				</div>
				<div v-else>
					<button type="button" class="btn btn-default" @click="buttonStartClientInfo">Enter your information</button>
				</div>
			</div>
			
			<div style="color: black; width: 50%; margin: 0 auto;">
				<div class="form-group">
					<!-- <label style="color: black;">Months</label>
					<input style="color: black;" class="form-control" type="number" min="6" max="108" name="years" step="6" @change="setSupportMonths" :value="getSupportMonths"> -->
					<label style="color: black;">Years</label>
					<input style="color: black;" class="form-control" type="number" min="0.5" max="9" step="0.5" name="years" @change="setSupportYears" :value="getSupportMonths/12">
				</div>
				<div style="color: black;" class="text-right">
					Estimate Total: ${{ getGrandTotal }}
					<br>
					<div class="btn-group">
						<button type="button" class="btn btn-info" @click="buttonPhoneSupport">
							<i class="fa fa-phone" aria-hidden="true"></i>
							&nbsp;Speak with Sales
						</button>
						<button type="button" class="btn btn-primary">
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

import {URL_ROOT,step_names} from '../store/values'

import moment from 'moment'
import velocity from 'velocity-animate'

export default {
	data () {
		return {
			current_plan: 0,
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
			'serverSetClient',
			'saveCart',
			'setCurrentPlan',
			'checkout',
		]),
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
			else {
				this.serverSetClient()
				this.checkout()
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
			console.log(Object.keys(this.getClientInfo).length>0)
			if (this.cart.length < 1) {
				this.buttonStartNewItem()
			}
			else if (Object.keys(this.getClientInfo).length<1) {
				this.buttonStartClientInfo()
			}
			else {
				this.saveCart(this.getClientInfo)
				$('#chatModal').modal('show')
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
				case 0:
					// Silver
					plan_name = 'silver'
					break;
				case 1:
					// Gold
					plan_name = 'gold'
					break;
				case 2:
					// Black
					plan_name = 'black'
					break;
			}
			// Product multiplier per plan e.g 1.0x
			let pp = product['price_'+plan_name]
			// Product Category multiplier e.g 1.2x
			let pm = product.category.price_multiplier
			// Plan base product price e.g $49/yr
			let pc = this.plans[this.current_plan].cost
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
		}
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
		}),
		getTotal() {
			let total = 0;
			for (let i=0; i<this.cart.length; i++) {
				total += this.getProductSubtotal(i)
			}
			return total
		},
		getGrandTotal() {
			let total = this.getTotal
			return this.numWithCommas(total)
		},
		textColorPlan() {
			return {'color': this.current_plan == 2 ? 'white' : 'black' }
		},
		cartStyle() {

		},
		cartHeaderStyle() {
			return {
				'background-color': this.plans[this.current_plan].color, 
				'color': this.current_plan == 2 ? 'white' : 'black'
			}
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



</style>