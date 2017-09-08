<template>
	
<div>
	<label>{{ step.placeholder }} </label> &nbsp;&nbsp;&nbsp;&nbsp;<label class="text-red" v-if="getErrors[step.form.name]"> {{ getErrors[step.form.name][0] }}</label>
	<input 
		:class="{'error-border': getErrors[step.form.name]}"
		:type="step.form.type" 
		:id="step.form.name" 
		:name="step.form.name" 
		:placeholder="step.placeholder" 
		class="form-control" 
		:value="get_form_input_value(step)" 
		@change="(el) => {
			setFormItem(el.target.value, step) 
		}"
		@keyup="(el) => {
			ValidateFormStepFunction(step, el.target.value)
		}"
	>
</div>

</template>

<script>

import { ValidateFormStep } from '../scripts/functions'

import {mapGetters, mapActions} from 'vuex'

export default {
	props: ['step'],
	mounted() {

	},
	methods: {
		...mapActions([
			'setCurrentItemProp',
			'setClientProp',
			'clearErrors',
			'clearError'
		]),
		ValidateFormStepFunction(step, value){
			let s = step.dest.split('.')
			
			if(s[0] == 'cart'){
				this.setCurrentItemProp({prop: s[s.length-1], data: value})
			}
			else if(s[0] == 'client'){
				this.setClientProp({prop: s[s.length-1], data: value})
			}
			else if(s[0] == 'payment'){
				this.setPaymentProp({prop: s[s.length-1], data: value})
			}
			

			let errors = ValidateFormStep(step, value)

			if(errors['valid'] == true){
				this.clearError(step.form.name)
			}
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
		}
	},
	computed: {
		...mapGetters([
			'getClientInfo',
			'getCurrentItemProp',
			'getErrors',
			'getCurrentItem'

		])
		
	}
}

</script>

<style lang="scss">

.error-border{
	border-color: #ff3434!important;

	&:focus {
		border-color: red!important;
    -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 8px rgba(255, 52, 52, 0.6);
    box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 8px rgba(255, 52, 52, 0.6);
    	
	}
}
	
</style>