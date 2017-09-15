<template>
	
<div>
	<br>
	<div class="container-fluid">
		<div style="margin:0px 0px 20px 0px; padding: 0px; background: rgba(255,255,255,0.23);" class="col-xs-12">
			<div style="margin:0px 0px 0px 0px; padding:10px 0px 10px 10px; background: rgba(0,0,0,0.16);" class="col-xs-12">
				<h3>{{ getPlan(getCurrentPlan).name }}</h3><h4>{{ writeOutSupportLength() }}</h4>
				
			</div>
			<div v-show="upsell != ''" style="margin:0px 0px 0px 0px; padding-top:0px; background: rgba(255,255,255,0.30);" class="col-xs-12">
				<!-- <button class="btn btn-lg btn-outline-info"><i style="color: #3285C4" class="fa fa-info-circle" aria-hidden="false"> &nbsp</i>{{ upsell }}</button> -->
			</div>
			<br>
			<!-- <h4>Cart Reference Code: {{ getCartReference }}</h4> -->
			<div style="margin:0px 0px 0px 0px; padding: 0px 0px 0px 0px;" class="col-xs-12">
				<table class="table table-hover table-outline" style="margin-bottom: 15px; border-bottom: 1px solid lightgray;">
<!-- 					<thead>
						<th style="padding-left:10px">Product</th>
						<th style="padding-left:10px">Price</th>
					</thead> -->
					<tbody>
						<tr v-for="(item, index) in getCart">
							<td style="color:white;" >{{ item.brand }} {{ item.model }}</td>
							<td style="color:white;" >${{ numWithCommas(getProductSubtotal(index)-getProductSubtotal(index)*getCurrentDiscount) }}</td>
						</tr>
					</tbody>
				</table>
			</div>
			<!-- <p class="pad-5">Cart Reference ID: {{ getCartReference }}</p>
			<div class="pad-5">
				<h4>Your information:</h4>
				<div v-if="Object.keys(getClientInfo).length > 0">
					<div v-for="key in Object.keys(getClientInfo)">
						{{key}}: {{getClientInfo[key]}}
					</div>
					<br>
					<button type="button" class="btn btn-link" @click="buttonEditClient">Edit</button>
				</div>
				<div v-else>
					<button type="button" class="btn btn-default" @click="buttonStartClientInfo">Enter your information</button>
				</div>
			</div> -->
			<div style="padding: 0px 0px 5px 7px">
			SubTotal: ${{ numWithCommas(getTotal) }}<br>
				%{{getCurrentDiscount*100}} Discount: &nbsp;
				- ${{numWithCommas(getTotal*getCurrentDiscount)}}<br>
				<span style="font-size: 1.2em;font-weight:700;">Payment Total: ${{ numWithCommas(getGrandTotal) }}</span>
			</div>
		</div>
		<div v-bind:style="form.buttonStyle"> 	
			<button v-on:keypress.enter.prevent style="white-space: normal;" type="button" v-for="btn in form.buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button>
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
			upsell: 'If you upgrade to Pure Gold you can get cloud support for free.'
		}
	},
	mounted() {

	},
	methods: {
		...mapActions([
			'setCurrentItemProp',
			'setClientProp'
		]),
		processAjaxResult(json) {
			return json['results']
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
			'getCartReference',
			'getProductSubtotal',
			'getTotal',
			'getGrandTotal',
			'getCurrentDiscount',
			'getSupportMonths'

		])
		
	}
}

</script>

<style lang="scss">

.table-hover>tbody>tr:hover {
    background-color: #CCCCCC;
}
	
</style>