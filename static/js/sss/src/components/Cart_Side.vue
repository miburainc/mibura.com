<template>

<div id="side-cart">
	<div :style="cartHeaderStyle">
		<div class="text-center" style="padding: 10px;">
			<h2 class="cart-tray" :style="textColorPlan">${{ numWithCommas(getGrandTotal) }}</h2>
		</div>
		<div>
			<div class="text-center">
				<button 
					type="button" 
					class="btn-plan" 
					v-for="(p, index) in plans" 
					:value="p.code"
					@click="setPlan"
					:style="{'color': p.color == '#000000' ? 'white' : 'black',backgroundColor: p.color}"
				>
					{{p.name}}
				</button>
			</div>
			
		</div>

	</div>

	<div style="color: black;">
		<h4 class="text-center">Cart</h4>
		<table class="table table-condensed table-striped">
			<thead>
				<th :style="cartHeaderStyle">Product</th>
				<th class="text-center" :style="cartHeaderStyle">Subtotal</th>
				<th class="text-center" :style="cartHeaderStyle">Options</th>
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
		<div class="btn-group btn-4">
			<button type="button" class="btn btn-sm btn-success" @click="buttonStartNewItem"><i class="fa fa-plus" aria-hidden="true"></i> Item</button>
			<button type="button" class="btn btn-sm btn-info" @click="buttonStartCloud"><i class="fa fa-cloud" aria-hidden="true"></i> Cloud</button>
			<button type="button" class="btn btn-sm btn-primary" @click="buttonGetEstimate"><i class="fa fa-upload" aria-hidden="true"></i> Quote</button>
			<button type="button" class="btn btn-sm btn-danger" @click="clear_cart"><i class="fa fa-times" aria-hidden="true"></i> Cart</button>
		</div>
		<br><br>
		<div class="btn-group btn-2">
			<button type="button" class="btn btn-info" @click="buttonPhoneSupport">
				<i class="fa fa-phone" aria-hidden="true"></i>
				&nbsp;Call Sales
			</button>
			<button type="button" class="btn btn-primary" @click="buttonGetPDF">
				<i class="fa fa-file-pdf-o" aria-hidden="true"></i>
				&nbsp;Get Quote
			</button>
		</div>
			
		<div v-if="get_cart_reference">
			<h4>Cart Reference Code: {{get_cart_reference}}</h4>
		</div>
		<div v-if="Object.keys(getClientInfo).length > 0" class="pad-10">
			<div>{{getClientInfo['first_name']}} {{getClientInfo['last_name'] }}</div>
			<div>{{getClientInfo['email']}}</div>
			<button type="button" class="btn btn-link" @click="buttonEditClient">Edit</button>
		</div>
		<div v-else class="pad-10">
			<button type="button" class="btn btn-default" @click="buttonStartClientInfo">Enter your information</button>
		</div>

		
		<div class="pad-10">
			<div class="form-group">
				<!-- <label style="color: black;">Months</label>
				<input style="color: black;" class="form-control" type="number" min="6" max="108" name="years" step="6" @change="setSupportMonths" :value="getSupportMonths"> -->
				<label style="color: black;">{{writeOutSupportLength}}</label>
				<input style="color: black;" class="form-control" type="number" min="0.5" max="9" step="0.5" name="years" @change="setSupportYears" :value="getSupportMonths/12">
			</div>
			<div class="text-right pad-10">
				SubTotal: ${{ numWithCommas(getTotal) }}<br>
				%{{getCurrentDiscount*100}} Discount: &nbsp;
				- ${{numWithCommas(getTotal*getCurrentDiscount)}}<br>
				<span style="font-size: 1.2em;font-weight:700;">Estimate Total: ${{ numWithCommas(getGrandTotal) }}</span>
			</div>
			<div class="btn-group btn-2">
				<button type="button" class="btn btn-default" data-toggle="modal" data-target="#termsModal">
					Terms &amp; Conditions
				</button>
				<button type="button" class="btn btn-success" @click="formPurchase">
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
		
		cartHeaderStyle() {
			let plan = this.getPlans(this.current_plan)
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

.pad-10 {
	padding: 10px;
}

#side-cart {
	margin-top: 15%;
	border-radius: 5px;
	border: 1px solid #000000;
	background-color: white;
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