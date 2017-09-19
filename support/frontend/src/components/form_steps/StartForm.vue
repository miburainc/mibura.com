<template>
	
<div>
	<br><br>
	<h2 class="text-center">
		Welcome to Mibura Smart Support
	</h2>
	<br>
	<h4 class="text-center">
		We're here to help! Just tell us what technologies you need support for.
	</h4>
	<br>
	<div v-bind:style="form.buttonStyle" class="container-fluid"> 	
		<button type="button" style="width:85%; display:block; padding: 15px 15px 15px 15px; margin:auto; margin-top: 20px; white-space: normal;" v-for="btn in form.buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button>
	</div>

</div>

</template>

<script>

import {mapGetters, mapActions} from 'vuex'

export default {
	props: ['form', 'buttonAction'],
	mounted() {

	},
	methods: {
		...mapActions({
			set_current_item_prop: 'setCurrentItemProp',
			set_current_form_step: 'setCurrentFormStep'
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