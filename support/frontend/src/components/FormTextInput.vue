<template>
	
<div>
	<label>{{ step.placeholder }} </label> &nbsp;&nbsp;&nbsp;&nbsp;<label class="text-red" v-if="getErrors[step.form.name]"> {{ getErrors[step.form.name][0] }}</label>
	<input 
		:style="{borderColor: (getErrors[step.form.name] ? 'red' : '#8493A8')}"
		:type="step.form.type" 
		:id="step.form.name" 
		:name="step.form.name" 
		:placeholder="step.placeholder" 
		class="form-control" 
		:value="get_form_input_value(step)" 
		@change="(el) => {
			setFormItem(el.target.value, step) 
		}"
	>
</div>

</template>

<script>

import {mapGetters, mapActions} from 'vuex'

export default {
	props: ['step'],
	mounted() {

	},
	methods: {
		...mapActions([
			'setCurrentItemProp',
			'setClientProp'
		]),
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

		])
		
	}
}

</script>

<style lang="scss">
	
</style>