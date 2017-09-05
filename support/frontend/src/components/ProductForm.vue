<template>
	
<div>
	<h2 class="text-center">
		Welcome to Mibura Smart Support
	</h2>
	<div class="form-group" ref="input">
		<div v-for="(step, index) in form">
			<div 
				v-for="data in step.data" 
				:style="{
					display: ((data.form.name == 'deviceage' || data.form.name == 'additionalinfo') && get_current_item_prop('verified') == undefined) ? 'none' : 'block'
				}"
			>
				<label>{{ data.placeholder }}</label>
				<input 
					@keyup.enter.prevent="formHandleEnter(index)"
					:data-index="index"
					:type="data.form.type" 
					:id="data.form.name" 
					:name="data.form.name" 
					:placeholder="data.placeholder" 
					class="form-control" 
					:value="get_form_input_value(data)" 
					@change="(el) => {
						setFormItem(el.target.value, data) 
					}"
				>
				
			</div>
			
		</div>
	</div>
	<div class="button-group">
		<button class="btn btn-lg btn-success">Add product to cart</button>
		<button class="btn btn-lg btn-info">Verify ACH</button>

		<button type="button" class="btn btn-lg btn-primary" @click="buttonGetEstimate"><i class="fa fa-upload" aria-hidden="true"></i> Enter Estimate ID</button>
	</div>
</div>

</template>

<script>

import {mapGetters, mapActions} from 'vuex'

export default {
	props: ['form'],
	mounted() {

	},
	methods: {
		...mapActions({
			set_current_item_prop: 'setCurrentItemProp',
		}),
		formHandleEnter(index) {
			// console.log(this.$refs)
			// console.log(this.$refs.input)
			// console.log(this.$refs.input.children[0])
			this.$refs.input.children[index+1].children[0].children[1].focus();

		},
		setFormItem (value, obj) {
			console.log(obj)
			let dest_array = obj.dest.split('.')

			if (dest_array[0] == "cart") {
				this.set_current_item_prop({prop: dest_array[2], data: value})
			}
			else if (dest_array[0] == "client") {
				if (dest_array[1] == "address") {
					this.set_client_prop({prop: dest_array[2], data: value})
				}
				else {
					this.set_client_prop({prop: dest_array[1], data: value})
				}
			}
			else if (dest_array[0] == "payment") {
				this.set_client_prop({prop: dest_array[1], data: value})
			}
		},
		buttonGetEstimate() {
			$('#estimateIdModal').modal('show')
		},
		get_form_input_value(obj) {
			let dest_array = obj.dest.split('.')
			let val = ""
			if (dest_array[0] == "cart") {
				val =  this.get_current_item_prop(dest_array[2])
			}
			else if (dest_array[0] == "client") {
				if (dest_array[1] == "address") {
					val = this.get_client_info[dest_array[2]]
				}
				else {
					val =  this.get_client_info[dest_array[1]]
				}
			}
			return val
		},
	},
	computed: {
		...mapGetters({
			get_client_info: 'getClientInfo',
			get_current_item_prop: 'getCurrentItemProp',

		})
		
	}
}

</script>

<style lang="scss">
	
</style>