<template>

<div id="sss-cart" style="background: transparent;">
	<div id="cart-header" class="row no-pad" :style="cartHeaderStyle">
		<div class="col-xs-12" style="padding-bottom:5px;">
			<div class="cart-tray" :style="textColorPlan" style="padding-left:15px;">Total: ${{ numWithCommas(getGrandTotal) }}
			<a class="btn btn-lg btn-info" :style="[textColorPlan, {'cursor': 'pointer', 'float': 'right'}]" style="margin-right:15px; padding: 3px 5px 3px 5px;" @click="scrollDown">View Cart</a></div>
		</div>
		<div class="col-xs-12 no-pad">
			<div class="no-pad">
					<button 
					class="btn-plan" 
					v-for="(p, index) in get_plans" 
					@click="setPlan" 
					:style="{
						color: p.color == '#000000' ? 'white' : 'black',
						background: p.code == current_plan ? 'transparent' : p.color,
						fontSize: '14px',

					}"
					:value="p.code">
						{{p.name}}
					</button>
			</div>
			<!-- <div class="no-pad">
				<button 
					type="button" 
					class="btn-plan text-center" 
					v-for="(p, index) in getPlans"
					:value="p.code"
					@click="setPlan"
					:style="{
						color: p.color == '#000000' ? 'white' : 'black',
						background: p.code == getCurrentPlan ? 'transparent' : p.color,
						fontSize: '11px',

					}"
				>
					{{p.name}}
				</button>
					
			</div> -->
		</div>
	</div>
	<div id="cart-body"style="width:75%; margin:auto; color: black; background: #E6E6E6; min-width: 375px;">
		<h1 class="text-center">Cart</h1>
		<table class="table table-condensed">
			<thead style="background: black;">
				<th>Product</th>
				<th class="text-center">Subtotal</th>
				<th class="text-right">Options</th>
			</thead>
			<tbody  style="background: white;">
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
							<!-- <button v-if="item.type != 'cloud'" type="button" class="btn btn-sm btn-warning" @click="editItem(item.sku, index)"><i class="fa fa-pencil" aria-hidden="true"></i></button>&nbsp; -->
							<button type="button" class="btn btn-sm btn-danger" @click="removeItem(item.id, index)"><i class="fa fa-times" aria-hidden="true"></i></button>
						</div>
					</td>
				</tr>
			</tbody>
		</table>
		<div class="btn-group btn-2">
			<button type="button" class="btn btn-sm btn-outline-info" @click="buttonStartNewItem"><i class="fa fa-plus" aria-hidden="true"></i> Item</button>
			<button type="button" class="btn btn-sm btn-outline-info" @click="buttonStartCloud"><i class="fa fa-plus" aria-hidden="true"></i> Cloud</button>
					
		</div>


		<div style="margin: 10px 0px 0px 0px">
			<button class="btn btn-sm" style="margin: 0px 0px 3px 0px; width: 21%; border: none; background: transparent;  text-align: center;" @click="setSupportYears(getSupportMonths - 6)"><i class="fa fa-minus-square fa-2x" style="color:#d9534f" aria-hidden="true"></i></button>
			
			<span><h4 style="margin: 2px; 0px 0px 0px; display:inline-block; width:56%; color: black; text-align: center;">{{writeOutSupportLength}}</h4></span>
			
			
			<button class="btn btn-sm" style="width: 18%; margin: 0px 0px 3px 0px; border: none; background: transparent; text-align: center;" @click="setSupportYears(getSupportMonths + 6)"><i class="fa fa-plus-square fa-2x" style="color:#00a25c" aria-hidden="true"></i></button>
		
			<input style="color: black;" class="form-control" type="hidden" min="0.5" max="9" step="0.5" name="years" @change="setSupportYears" :value="getSupportMonths/12">
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
			this.setCurrentFormStep(step_names.item)
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
			if (this.current_plan == 'black') {
				return {
					'padding-top': '5px',
					'background-color': '#000000', 
    				'background-size': '6px 8px',
    				'color': this.current_plan == 'black' ? 'white' : 'black'
				}
			}
			
			else if (this.current_plan == 'gold') {
				return {
					// 'background-color': plan.color, 
					'padding-top': '5px',
					'background-color': '#FFFFFF',
					'background-image':
						'linear-gradient(90deg,rgba(225,190,77,1) 0%,rgba(243, 198, 66,0.6)  39%,rgba(225,190,77,1) 75%)',
    				'color': this.current_plan == 'black' ? 'white' : 'black'
				}
			}
			else if (this.current_plan == 'silver') {
				return {
					// 'background-color': plan.color, 
					'padding-top': '5px',
					'background': '#aaa',
					'background-image':
						'linear-gradient(90deg,rgba(255,255,255,0) 0%,rgba(255,255,255,0.6)  39%,rgba(255,255,255,0) 75%)',
    				'color': this.current_plan == 'black' ? 'white' : 'black'
				}
			}
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
	padding: 0px;
	padding-bottom: 100px;
}

#sss-cart {
	background: transparent;
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