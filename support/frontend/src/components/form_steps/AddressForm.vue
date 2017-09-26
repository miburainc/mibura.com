<template>
	
<div>
	<div class="form-group" v-on:keyup.enter="submitForm">

		<div ref="input" v-for="(step, index) in fields" 
			:style="{
					display: ((step.form.name == 'deviceage' || step.form.name == 'additionalinfo') && getCurrentItemProp('verified') == true) ? 'none' : 'block'
				}">
			
			<form-text-input :step="step"></form-text-input>

		</div>
		<div v-bind:style="buttonStyle"> 	
			<button style="margin-right:3px; white-space: normal;" v-on:keypress.enter.prevent type="button" v-for="btn in buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button>
		</div>
	</div>
</div>

</template>

<script>

import {mapGetters, mapActions} from 'vuex'

import FormTextInput from '../FormTextInput.vue'

export default {
	components: {
		'form-text-input': FormTextInput
	},
	props: ['form', 'buttonAction'],
	data() {
		return {
			fields: [
				{
					placeholder: "Street",
					src: "",
					dest: "client.address.street",
					required: true,
					validate: {
						type: "text", 
						min: 3,
					},
					form: {
						type: "text",
						name: "street1",
					}
				},
				{
					placeholder: "Street 2",
					src: "",
					dest: "client.address.street2",
					required: false,
					validate: {},
					form: {
						type: "text",
						name: "street2",
					}
				},
				{
					placeholder: "City",
					src: "",
					dest: "client.address.city",
					required: true,
					validate: {
						type: "text", 
						min: 3,
					},
					form: {
						type: "text",
						name: "city",
					}

				},
				{
					placeholder: "State",
					src: "",
					dest: "client.address.state",
					required: true,
					validate: {
						min: 2,
					},
					form: {
						type: "text",
						name: "state",
					}
				},
				{
					placeholder: "Country",
					src: "",
					dest: "client.address.country",
					required: true,
					validate: {
						type: "text",
						min: 2,
					},
					form: {
						type: "text",
						name: "country",
					}
				},
				{
					placeholder: "Zipcode",
					src: "",
					dest: "client.address.zipcode",
					required: true,
					validate: {
						type: "number",
						min: 5,
						max: 6,
					},
					form: {
						type: "number",
						name: "zipcode",
					}
				},
			],
			buttons: [
				{
					label: "Back",
					class: "btn btn-lg btn-default",
					script: "back"
				},
				{
					label: "Review Cart",
					class: "btn btn-lg btn-success",
					script: "next"

				},
			],
			title: "Billing Address",
			text: "",
			error: "",
			step: 2,
			buttonStyle: "margin-top: 14px;"
		}
	},
	mounted() {

	},
	methods: {
		...mapActions([
			'setCurrentItemProp',
			'setClientProp'
		]),
		submitForm(){
			this.buttonAction(null, "next")
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

		])
		
	}
}

</script>

<style lang="scss">
	
</style>