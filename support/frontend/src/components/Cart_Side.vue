<template>

<div id="side_cart">
	<div :style="cartHeaderStyle">
		<div class="text-center" style="padding: 10px;">
			<h2 class="cart-tray" :style="textColorPlan">${{ numWithCommas(getGrandTotal) }}</h2>
		</div>
		<div>
			<div class="btn-3">
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
					
			</div>
			
		</div>

	</div>

	<div style="color: black;">
		<h4 class="text-center">Cart</h4>
		<table id="cart-table-header" class="table table-condensed table-striped">
			<thead :style="cartHeaderStyle">
				<th style="padding-left: 15px">Product</th>
				<th class="text-right">Subtotal</th>
				<th class="text-right" style="padding-right: 15px">Options</th>
			</thead>
		</table>
		<div style="max-height:150px;overflow:auto;margin-bottom:0px;">
			<table class="table table-striped table-condensed table-hover">
				<tbody class="cart-table-body">
					<tr v-if="this.getCart.length < 1" class="text-center">
						<td colspan="4">None</td>
					</tr>
					<tr v-else v-for="(item, index) in getCart">
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
		<!-- <button type="button" style="width:100%;" class="btn btn-xs btn-danger" @click="clear_cart"><i class="fa fa-times" aria-hidden="true"></i> Clear Cart</button> -->
		
		<div class="btn-group btn-2">
			<button type="button" class="btn btn-sm btn-success" @click="buttonStartNewItem"><i class="fa fa-plus" aria-hidden="true"></i> Item</button>
			<button type="button" class="btn btn-sm btn-info" @click="buttonStartCloud"><i class="fa fa-plus" aria-hidden="true"></i> Cloud</button>
			
			
		</div>
		<br><br>
		<!-- <div class="btn-group btn-2">
			<button type="button" class="btn btn-sm btn-info" @click="buttonPhoneSupport">
				<i class="fa fa-phone" aria-hidden="true"></i>
				&nbsp;Call Sales
			</button>
			<button type="button" class="btn btn-sm btn-primary" @click="buttonGetPDF">
				<i class="fa fa-file-pdf-o" aria-hidden="true"></i>
				&nbsp;Get Quote
			</button>

		</div> -->
			
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

		<div class="pad-5">
			<div class="text-right pad-10">
				<!-- SubTotal: ${{ numWithCommas(getTotal) }}<br> -->
				%{{getCurrentDiscount*100}} Discount: &nbsp;
				- ${{numWithCommas(getTotal*getCurrentDiscount)}}<br>
				<!-- <span style="font-size: 1.2em;font-weight:700;">Estimate Total: ${{ numWithCommas(getGrandTotal) }}</span> -->
			</div>
			<!-- <div class="btn-group btn-2">
				<button type="button" class="btn btn-sm btn-default" data-toggle="modal" data-target="#termsModal">
					Terms &amp; Conditions
				</button>
				<button type="button" class="btn btn-sm btn-success" @click="formPurchase">
					<i class="fa fa-check" aria-hidden="true"></i>
					&nbsp;Purchase
				</button>
			</div> -->
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
			if (this.getCart.length < 1) {
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
			else if (!this.getPaymentToken) {
				this.addNotification({
					type: 'warning',
					message: 'Please fill out your payment information!'
				})
				this.buttonStartPayment()
			}
			else if (!this.getAcceptedTerms) {
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
			this.setCurrentFormStep(step_names.item)
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
		buttonGetPDF() {
			if (this.getCart.length < 1) {
				this.addNotification({
					type: 'warning',
					message: 'Please add items to your cart!'
				})
				this.buttonStartNewItem()
			}
			else if (Object.keys(this.getClientInfo).length<10) {
				this.addNotification({
					type: 'warning',
					message: 'Please provide your contact information.'
				})
				this.buttonStartClientInfo()
			}
			else {
				if (this.getCartChanged) {
					// Reset pdf to nothing
					this.setEstimatePdfFile(null);
					// Send request for new pdf file
					this.saveCart(this.getClientInfo)
						.then(() => {
							this.serverGetEstimatePdf()
						})
				}
				$('#pdfModal').modal('show')
			}
		},
		clear_cart() {
			if (confirm("Are you sure you want to clear your cart?") == true) {
				this.clearCart()
			}
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
		...mapGetters([
			'numWithCommas',
			'getCart',
			'getPlans',
			'getPlan',
			'getSupportMonths',
			'getMultiplier',
			'getClientInfo',
			'getPaymentToken',
			'getCartReference',
			'getAcceptedTerms',
			'getCurrentPlan',
			'getTotal',
			'getProductSubtotal',
			'getGrandTotal',
			'getCurrentDiscount',
			'getCartChanged',
		]),

		textColorPlan() {
			return {'color': this.getCurrentPlan == 'black' ? 'white' : 'black' }
		},

		cartPlanBlackBackground() {
			return {
				'background-color': '#000000', 
				'background-image': 'repeating-linear-gradient(-26deg, rgba(255,255,255, 0.02), rgba(255,255,255, 0.15) 2px, transparent 3px, transparent 7px)',
				'background-size': '6px 8px',
			}
		},
		
		cartHeaderStyle() {
			let plan = this.getPlan(this.getCurrentPlan)
			if (this.getCurrentPlan == 'black') {
				return {
					'padding-top': '10px',
					'background-color': '#000000', 
					'background-image': 'repeating-linear-gradient(-26deg, rgba(255,255,255, 0.02), rgba(255,255,255, 0.12) 2px, transparent 3px, transparent 7px)',
    				'background-size': '6px 8px',
    				'color': this.getCurrentPlan == 'black' ? 'white' : 'black'
				}
			}
			
			else if (this.getCurrentPlan == 'gold') {
				return {
					// 'background-color': plan.color, 
					'padding-top': '10px',
					'background-image':
						'linear-gradient(90deg,rgba(225,190,77,1) 0%,rgba(243, 198, 66,0.6)  39%,rgba(225,190,77,1) 75%)',
    				'color': this.getCurrentPlan == 'black' ? 'white' : 'black'
				}
			}
			else if (this.getCurrentPlan == 'silver') {
				return {
					// 'background-color': plan.color, 
					'padding-top': '10px',
					'background': '#aaa',
					'background-image':
						'linear-gradient(90deg,rgba(255,255,255,0) 0%,rgba(255,255,255,0.6)  39%,rgba(255,255,255,0) 75%)',
    				'color': this.getCurrentPlan == 'black' ? 'white' : 'black'
				}
			}
			return {
				'padding-top': '10px',
				'background-color': plan.color, 
				'color': this.getCurrentPlan == 'black' ? 'white' : 'black'
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

// CSS texture style from codepen.io
.pattern3 {
    background-image: repeating-linear-gradient(-26deg, rgba(255,255,255, 0.25), rgba(255,255,255, 0.25) 2px, transparent 3px, transparent 7px);
    background-size: 6px 8px;
}

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