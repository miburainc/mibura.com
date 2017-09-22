<template>
	
<div>
	<h1>Success!</h1>
	<h4>Please return and verify ach amounts deposited in your bank account.</h4>
	<div v-if="getEstimatePDF">
		<div id="pdf">
				<object width="100%" height="500" type="application/pdf" :data="getEstimatePDF" id="pdf_content">
				<p>Error, reciept cannot be displayed at this time.</p>
				</object>
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
		if (!this.getEstimatePDF) {
			this.serverGetEstimatePdf()
		}
	},
	methods: {
		...mapActions([
			'setCurrentItemProp',
			'setClientProp',
			'serverGetEstimatePdf'
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
			'getEstimatePDF'

		])
		
	}
}

</script>

<style lang="scss">
	
</style>