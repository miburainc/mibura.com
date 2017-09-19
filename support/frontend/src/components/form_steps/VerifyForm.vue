<template>
	
<div>
	<br>
	<div class="container-fluid">
		<div style="margin:0px 0px 10px 0px; padding: 20px; background: rgba(255,255,255,0.23);" class="col-xs-12">
			<h3>{{ getPlan(getCurrentPlan).name }}</h3>
			<h4>Cart Reference Code: {{ getCartReference }}</h4>
			<table class="table table-hover table-outline" style="border-bottom: 3px solid white;border-top: 3px solid white">

				<tbody>
					<tr v-for="(item, index) in getCart">
						<td style="color:white;" >{{ item.brand }} {{ item.model }}</td>
						<td style="color:white; text-align:right;" >${{ numWithCommas(getProductSubtotal(index)-getProductSubtotal(index)*getCurrentDiscount) }}</td>
					</tr>
				</tbody>
			</table>
			<div class="row">
				<div class="col-md-7" style=""></div>
				<div class="col-xs-12 col-md-5" style="padding: 0px 22px 15px 7px; text-align:right; ">
					<p style="margin:0px">SubTotal:  ${{ numWithCommas(getTotal) }}</p>
					<p style="margin:0px">%{{getCurrentDiscount*100}} Discount:
					 ${{numWithCommas(getTotal*getCurrentDiscount)}}</p>
					<span style="font-size: 1.5em;font-weight:700;">Payment Total: ${{ numWithCommas(getGrandTotal) }}</span>
				</div>
			</div>
			<div v-if="Object.keys(getClientInfo).length > 0" class="row" style="padding:15px 0px 15px 0px; margin: 12px 10px 0px 10px; border-bottom: 1px solid lightgray;border-top: 1px solid lightgray">
				
				<div class="col-lg-4"><h4>Personal Information</h4><br></div>
				
				<div class="col-lg-3">
					{{getClientInfo['first_name']}} {{getClientInfo['last_name'] }}<br>
					{{getClientInfo['email']}}<br>
					{{getClientInfo['company']}}<br>
					{{getClientInfo['phone']}}
				</div>
				<div class="col-lg-3">
					{{getClientInfo['street']}}, {{getClientInfo['street2']}}<br>
					{{getClientInfo['city']}}, {{getClientInfo['state']}}<br>
					{{getClientInfo['zipcode']}}, {{getClientInfo['country']}}<br>
				</div>
				<div class="col-lg-2"><a href="#" style="color:lightblue;">Change</a></div>
			</div>

			<!-- <div v-if="Object.keys(getPaymentInfo).length > 0" class="pad-10 row" style="padding:10px 0px 10px 0px; margin: 0px 10px 0px 10px; border-bottom: 1px solid lightgray">
				
				<div class="col-xs-4"><h4>Payment Method</h4></div>
				
				<div class="col-xs-3">
					<p v-if="getPaymentInfo['bankName']">{{ getPaymentInfo['bankName'] }}<br></p>
					<p v-else=""
				</div>
				<div class="col-xs-3">

				</div>
				<div class="col-xs-2">
					<a href="#" style="color:lightblue;">Change</a>
				</div>
			</div> -->

			
			<div style="text-align:center; margin-top:10px;">
			<h4>If you have any questions about your order please call us at 1.800.862.5144.</h4>
			</div>
			<br>
			<div style="text-align:center">
				
				<a v-if="getAcceptedTerms" role="button" class="btn btn-lg btn-success" href="#" data-toggle="modal" data-target="#termsModal">Terms Accepted &nbsp;&nbsp;<i aria-hidden="true" class="fa fa-check"></i></a>
				<a v-else role="button" style="color:lightblue;" class="btn btn-lg btn-outline-info" href="#" data-toggle="modal" data-target="#termsModal">Terms &amp; Conditions</a>&nbsp;&nbsp;&nbsp;&nbsp;

				
				<!-- <label style="font-size: 20px; color: lightblue;">

					<input style="height:19px; width:19px;" @change="(e) => {setAcceptedTerms(e.target.checked)}" type="checkbox" :checked="getAcceptedTerms">
					Accept
				</label> -->
			</div>
		</div>
		<div v-bind:style="form.buttonStyle"> 	
			<button v-if="!getPaymentProcessing" v-on:keypress.enter.prevent type="button" style="white-space: normal;" v-for="btn in form.buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script);}">{{btn.label}}</button><button v-if="getPaymentProcessing" style="width:100%" class="btn btn-lg btn-success">Processing <i class="fa fa-circle-o-notch fa-spin" style="font-size:24px"></i></button>
		</div>
	</div>
</div>

</template>

<script>

import {mapGetters, mapActions} from 'vuex'

import Autocomplete from 'vue2-autocomplete-js';

export default {

	props: ['form', 'buttonAction'],
	data(){
		return{
			processing: false
		}
	},
	mounted() {

	},
	methods: {
		...mapActions([
			'setCurrentItemProp',
			'setClientProp',
			'setCurrentFormStep',
			'serverSetClient',
			'saveCart',
			'checkout',
			'setAcceptedTerms',
		]),
		setTerms(value){
			this.setAcceptedTerms(value)
			console.log(value)
			document.getElementById('termsCheckbox').checked = value
		},
		processAjaxResult(json) {
			return json['results']
		},
		setFormItemAutoselect (obj, name) {
			console.log("Name: " + name)
			console.log("Obj: ", obj)
			this.setCurrentItemProp({ prop: "brand", data: obj["brand"] })
			this.setCurrentItemProp({ prop: "model", data: obj["model"] })
			this.setCurrentItemProp({ prop: 'verified', data: true })

			// if (name == "model") {
			// 	this.addProduct({id: obj.model, data: obj})
			// 	// this.$set(this.product_info, obj['model'], obj)
			// }
		},
		setFormItem (value, obj) {
			console.log(obj)
			let dest_array = obj.dest.split('.')

			if (dest_array[0] == "cart") {
				this.setCurrentItemProp({prop: dest_array[2], data: value})
			}
			else if (dest_array[0] == "client") {
				if (dest_array[1] == "address") {
					this.setClientProp({prop: dest_array[2], data: value})
				}
				else {
					this.setClientProp({prop: dest_array[1], data: value})
				}
			}
			else if (dest_array[0] == "payment") {
				this.setClientProp({prop: dest_array[1], data: value})
			}
		},
		buttonGetEstimate() {
			$('#estimateIdModal').modal('show')
		},
		get_form_input_value(obj) {
			let dest_array = obj.dest.split('.')
			let val = ""
			if (dest_array[0] == "cart") {
				val =  this.getCurrentItemProp(dest_array[2])
			}
			else if (dest_array[0] == "client") {
				if (dest_array[1] == "address") {
					val = this.getClientInfo[dest_array[2]]
				}
				else {
					val =  this.getClientInfo[dest_array[1]]
				}
			}
			return val
		},
		resetVerified(){
			this.setCurrentItemProp({ prop: 'verified', data: false })
		}
	},
	computed: {
		...mapGetters([
			'getClientInfo',
			'getCurrentItemProp',
			'getErrors',
			'numWithCommas',
			'getPlan',
			'getCurrentPlan',
			'getCart',
			'getCurrentFormStep',
			'getCartReference',
			'getProductSubtotal',
			'getTotal',
			'getGrandTotal',
			'getCurrentDiscount',
			'getPaymentToken',
			'getPaymentInfo',
			'getAcceptedTerms',
			'getPaymentProcessing'

		])
		
	}
}

</script>

<style lang="scss">

</style>