<template>
	
<div>
	<br>
	<div class="container-fluid">
		<div style="margin:0px 0px 20px 0px; padding: 20px; background: rgba(255,255,255,0.23);" class="col-xs-12">
			<h3>{{ getPlan(getCurrentPlan).name }}</h3>
			<h4>Cart Reference Code: {{ getCartReference }}</h4>
			<table class="table table-hover table-outline">
				<thead>
					<th>Product</th>
					<th>Price</th>
				</thead>
				<tbody>
					<tr v-for="(item, index) in getCart">
						<td style="color:white;" >{{ item.brand }} {{ item.model }}</td>
						<td style="color:white;" >${{ numWithCommas(getProductSubtotal(index)-getProductSubtotal(index)*getCurrentDiscount) }}</td>
					</tr>
				</tbody>
			</table>
			<div v-if="Object.keys(getClientInfo).length > 0" class="pad-10" style="display:inline-block;">
				<div class="col-xs-6">
					{{getClientInfo['first_name']}} {{getClientInfo['last_name'] }}<br>
					{{getClientInfo['email']}}<br>
					{{getClientInfo['company']}}<br>
					{{getClientInfo['phone']}}
				</div>
				<div class="col-xs-6">
					{{getClientInfo['street']}}, {{getClientInfo['street2']}}<br>
					{{getClientInfo['city']}}, {{getClientInfo['state']}}<br>
					{{getClientInfo['zipcode']}}, {{getClientInfo['country']}}<br>
				</div>
			</div>
			<br><br><br>
			<div>
			SubTotal: ${{ numWithCommas(getTotal) }}<br>
				%{{getCurrentDiscount*100}} Discount: &nbsp;
				- ${{numWithCommas(getTotal*getCurrentDiscount)}}<br>
				<span style="font-size: 1.2em;font-weight:700;">Payment Total: ${{ numWithCommas(getGrandTotal) }}</span>
			</div>
			
			<br>
			<a role="button" class="btn btn-lg btn-outline-info" href="#" data-toggle="modal" data-target="#termsModal">Terms &amp; Conditions</a>
			<br>
			<label style="font-size: 20px; color: lightblue;">
				<input style="height:19px; width:19px;" @change="(e) => {setAcceptedTerms(e.target.checked)}" type="checkbox" value="">
				Accept
			</label>
			
		</div>
		<div v-bind:style="form.buttonStyle" class="btn-2-round"> 	
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
			'getPaymentToken'

		])
		
	}
}

</script>

<style lang="scss">
	
</style>