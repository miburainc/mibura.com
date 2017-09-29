<template>
	
<div v-on:keyup.enter="submitForm">
	<br><br>
	<h2 class="text-center">
		Welcome to Mibura Smart Support
	</h2>
	<br>
	<h4 class="text-center">
		We're here to offer 3rd party hardware, software, and cloud support. Please answer a few quick questions and we will tailor a support plan that will fit your needs.
	</h4>
	<br>
	<div class="btn-container container-fluid"> 	
		<button type="button" v-for="btn in buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button>
	</div>

</div>

</template>

<script>

import {mapGetters, mapActions} from 'vuex'

export default {
	props: ['form', 'buttonAction'],
	data() {
		return {
			buttons: [
				{
					label: "New Customer",
					class: "btn btn-lg btn-success",
					script: "next"
				},
				{
					label: "Already have a quote? Click here to checkout",
					class: "btn btn-lg btn-default",
					script: "returning"
				}
			],
			buttonStyle: ""
		}
	},
	mounted() {

	},
	methods: {
		...mapActions({
			set_current_item_prop: 'setCurrentItemProp',
			set_current_form_step: 'setCurrentFormStep'
		}),
		submitForm(){
			this.buttonAction(null, "next")
		},
		formHandleEnter(index) {
			// console.log(this.$refs)
			// console.log(this.$refs.input)
			// console.log(this.$refs.input.children[0])
			this.$refs.input.children[index+1].children[0].children[1].focus();

		},
		setFormItem (value, obj) {
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
	},
	computed: {
		...mapGetters([
			'getClientInfo',
			'getCurrentItemProp',
		]),
	}
}

</script>

<style lang="scss">
	

.btn-container {
	text-align: center;
	margin-top: 12px;

	button {
		width: 85%;
		display: block;
		padding: 15px 15px 15px 15px;
		margin: auto;
		margin-top: 20px;
		white-space: normal;
	}
}

</style>