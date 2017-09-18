<template>

<div id="side_cart" style="min-width:270px;">
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
		<!-- <h4 class="text-center">Cart</h4>
		<table id="cart-table-header" class="table table-condensed table-striped">
			<thead :style="cartHeaderStyle">
				<th style="padding-left: 15px">Product</th>
				<th class="text-right">Subtotal</th>
				<th class="text-right" style="padding-right: 15px">Options</th>
			</thead>
		</table> -->
		<div class="btn-group btn-2">
			<button type="button" class="btn btn-sm btn-outline-info" style="border: none" @click="buttonStartNewItem"><i class="fa fa-plus" aria-hidden="true"></i> Item</button>
			<button type="button" class="btn btn-sm btn-outline-info" style="border: none" @click="buttonStartCloud"><i class="fa fa-plus" aria-hidden="true"></i> Cloud</button>
		</div>
		<div v-show="this.getCart.length > 0" style="max-height:150px;overflow:auto;margin: 0px; padding:0px;">
			<table class="table table-striped table-condensed table-hover" style="padding:0px; margin:0px; border-bottom: 1px solid lightgray">
				<tbody class="cart-table-body">
					<!-- <tr v-if="this.getCart.length < 1" class="text-center">
						<td colspan="4">None</td>
					</tr> -->
					<!-- <tr v-else v-for="(item, index) in getCart"> -->
					<tr v-for="(item, index) in getCart">
						<td>
							<i v-if="item.type=='cloud'" class="fa fa-cloud" aria-hidden="true"></i>
							{{item.brand}} {{item.model}}
						</td>
						<td class="text-center">
							${{ numWithCommas(getProductSubtotal(index)-getProductSubtotal(index)*getCurrentDiscount) }}
						</td>
						<td class="text-right">
							<div class="btn-group">
								<!-- <button v-if="item.type != 'cloud'" type="button" class="btn btn-xs btn-warning" @click="editItem(item.sku, index)"><i class="fa fa-pencil" aria-hidden="true"></i></button>&nbsp; -->
								<button type="button" class="btn btn-xs btn-danger" @click="removeItem(item.id, index)"><i class="fa fa-times" aria-hidden="true"></i></button>
							</div>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
		<!-- <button type="button" style="width:100%;" class="btn btn-xs btn-danger" @click="clear_cart"><i class="fa fa-times" aria-hidden="true"></i> Clear Cart</button> -->
		
		
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
			
		<div style="background: #DEDEDE; margin-bottom: 110px;">

			<button class="btn btn-sm" style="margin: 0px 0px 3px 0px; width: 15%; border: none; background: transparent;  text-align: center;" @click="setSupportYears(getSupportMonths - 6)"><i class="fa fa-minus-square fa-2x" style="color:#d9534f" aria-hidden="true"></i></button>
			
			<span><h4 style="margin: 2px; 0px 0px 0px; display:inline-block; width:68%; color: black; text-align: center;">{{writeOutSupportLength}}</h4></span>
			
			
			<button class="btn btn-sm" style="width: 11%; margin: 0px 0px 3px 0px; border: none; background: transparent; text-align: center;" @click="setSupportYears(getSupportMonths + 6)"><i class="fa fa-plus-square fa-2x" style="color:#00a25c" aria-hidden="true"></i></button>
		
				
			<input style="color: black;" class="form-control" type="hidden" min="0.5" max="9" step="0.5" name="years" @change="setSupportYears" :value="getSupportMonths/12">
			
		</div>

		<!-- <div class="pad-5">
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
		</div> -->
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
			windowWidth: 0,
			windowHeight: 0,
		}
	},
	mounted() {
		this.$nextTick(function() {
			window.addEventListener('resize', this.getWindowWidth);
			window.addEventListener('resize', this.getWindowHeight);

			//Init
			this.getWindowWidth()
			this.getWindowHeight()
		})
	},
	beforeDestroy() {
		window.removeEventListener('resize', this.getWindowWidth);
		window.removeEventListener('resize', this.getWindowHeight);
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

		getWindowWidth(event) {
			this.windowWidth = $(window).width()
		},

		getWindowHeight(event) {
			this.windowHeight = $(window).height()
		},

		setPlan(el) {
			let val = el.target.value
			switch(val) {
				case 'silver':
					this.addNotification({
						type: 'success',
						message: 'Pro Silver provides 4 hour response for the lowest price!'
						// message: 'Pro Silver provides 4 hour response for the lowest price! <a href="/support#plan-comparison" target="_blank">Click here to see more!</a>'
					})
					break;
				case 'gold':
					this.addNotification({
						type: 'success',
						message: 'Pure Gold provides 15 min response and free cloud support!'
						// message: 'Pure Gold provides 15 min response and free cloud support! <a href="/support#plan-comparison" target="_blank">Click here to see more!</a>'
					})
					break;
				case 'black':
					this.addNotification({
						type: 'success',
						message: 'Carbon Black provides 15 min response and a dedicated security & compliance team!'
						// message: 'Carbon Black provides 15 min response and a dedicated security & compliance team! <a href="/support#plan-comparison" target="_blank">Click here to see more!</a>'
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
			let result = {
				'z-index': 100,
				'position': this.windowWidth < 977 ? 'fixed' : 'static',
				'bottom': this.windowWidth < 977 ? '0px' : 'auto',
				'left': this.windowWidth < 977 ? '0px' : 'auto',
				'right': this.windowWidth < 977 ? '0px' : 'auto',
			}
			if (this.getCurrentPlan == 'black') {
				return Object.assign(result, {
					'padding-top': '10px',
					'background-color': '#000000', 
					'background-image': 'repeating-linear-gradient(-26deg, rgba(255,255,255, 0.02), rgba(255,255,255, 0.12) 2px, transparent 3px, transparent 7px)',
    				'background-size': '6px 8px',
    				'color': this.getCurrentPlan == 'black' ? 'white' : 'black'
				})
			}
			
			else if (this.getCurrentPlan == 'gold') {
				return Object.assign(result, {
					// 'background-color': plan.color, 
					'padding-top': '10px',
					'background-image':
						'linear-gradient(90deg,rgba(225,190,77,1) 0%,rgba(243, 198, 66,0.6)  39%,rgba(225,190,77,1) 75%)',
    				'color': this.getCurrentPlan == 'black' ? 'white' : 'black'
				})
			}
			else if (this.getCurrentPlan == 'silver') {
				return Object.assign(result, {
					// 'background-color': plan.color, 
					'padding-top': '10px',
					'background': '#aaa',
					'background-image':
						'linear-gradient(90deg,rgba(255,255,255,0) 0%,rgba(255,255,255,0.6)  39%,rgba(255,255,255,0) 75%)',
    				'color': this.getCurrentPlan == 'black' ? 'white' : 'black'
				})
			}
			return Object.assign(result, {
				'padding-top': '10px',
				'background-color': plan.color, 
				'color': this.getCurrentPlan == 'black' ? 'white' : 'black'
			})
		},
		writeOutSupportLength() {
			let str = ""
			let lenArray = String(this.getSupportMonths / 12).split('.')
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
	},

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

.btn-plan {
	border-radius: 0px;
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