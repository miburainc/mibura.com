<template>
	
<div>
	<br>
	<div class="container-fluid">
		<div style="margin:0px 0px 20px 0px; padding: 0px; background: rgba(255,255,255,0.23);" class="col-xs-12">
			<div style="margin:0px 0px 0px 0px; padding:10px 0px 10px 10px; background: rgba(0,0,0,0.16);" class="col-xs-12">
				<h3>{{ getPlan(getCurrentPlan).name }}</h3>
			</div>
			<div v-show="upsell != ''" style="margin:0px 0px 0px 0px; padding-top:0px; background: rgba(255,255,255,0.30);" class="col-xs-12">
				<button class="btn btn-lg btn-outline-info"><i style="color: #3285C4" class="fa fa-info-circle" aria-hidden="false"> &nbsp</i>{{ upsell }}</button>
			</div>
			<br>
			<!-- <h4>Cart Reference Code: {{ getCartReference }}</h4> -->
			<div style="margin:0px 0px 10px 0px; padding: 10px 0px 0px 0px;" class="col-xs-12">
				<table class="table table-hover table-outline">
					<thead>
						<th style="padding-left:10px">Product</th>
						<th style="padding-left:10px">Price</th>
					</thead>
					<tbody>
						<tr v-for="(item, index) in getCart">
							<td style="color:white;" >{{ item.brand }} {{ item.model }}</td>
							<td style="color:white;" >${{ numWithCommas(getProductSubtotal(index)-getProductSubtotal(index)*getCurrentDiscount) }}</td>
						</tr>
					</tbody>
				</table>
			</div>
			<div style="padding: 0px 0px 5px 7px">
			SubTotal: ${{ numWithCommas(getTotal) }}<br>
				%{{getCurrentDiscount*100}} Discount: &nbsp;
				- ${{numWithCommas(getTotal*getCurrentDiscount)}}<br>
				<span style="font-size: 1.2em;font-weight:700;">Payment Total: ${{ numWithCommas(getGrandTotal) }}</span>
			</div>
		</div>
		<div v-bind:style="form.buttonStyle" class="btn-3-round"> 	
			<button v-on:keypress.enter.prevent type="button" v-for="btn in form.buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button>
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

		])
		
	}
}

</script>

<style lang="scss">
	
</style>