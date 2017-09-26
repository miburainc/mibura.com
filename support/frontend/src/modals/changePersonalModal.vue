<template>
	<div v-on:keyup.enter="submitForm" class="modal" id="ChangePersonalModal" tabindex="1" role="dialog" aria-labelledby="myModalLabel">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
					<h4 class="modal-title" id="myModalLabel">Change Personal Information</h4>
					<label v-if="checkErrors" style="color:red">Invalid entry</label>
				</div>
				<div class="modal-body">
					<div ref="input" v-for="(step, index) in fields">
						<form-text-input :step="step"></form-text-input>
					</div>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-primary" @click="submitForm">Submit</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

import {mapGetters, mapActions} from 'vuex'

import { ValidateFormSteps } from '../scripts/functions'
import { forEachValue } from '../scripts/util'

import FormTextInput from '../components/FormTextInput.vue'

export default {
	props: ['buttonAction'],
	components:{
		FormTextInput
	},
	data() {
		return {
			fields: [
				{
					placeholder: "First Name",
					dest: "client.first_name",
					required: true,
					validate: {
						type: "text", 
						min: 3
					},
					form: {
						type: "text",
						name: "firstname",
					}
				},
				{
					placeholder: "Last Name",
					src: "",
					dest: "client.last_name",
					required: true,
					validate: {
						type: "text", 
						min: 3
					},
					form: {
						type: "text",
						name: "lastname",
					}
				},
				{
					placeholder: "Company",
					src: "",
					dest: "client.company",
					required: true,
					validate: {
						type: "text", 
						min: 3
					},
					form: {
						type: "text",
						name: "company",
					}
				},
				{
					placeholder: "Phone Number",
					src: "",
					dest: "client.phone",
					required: true,
					validate: {
						type: "phone",
						min: 6,
					},
					form: {
						type: "text",
						name: "phonenumber",
					}
				},
				{
					placeholder: "Email Address",
					src: "",
					dest: "client.email",
					required: true,
					validate: {
						type: "email",
					},
					form: {
						type: "text",
						name: "email",
					}
				},
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
			]
		}
	},
	mounted() {

	},
	methods: {
		...mapActions([
			'setClientProp',
			'clearError',
			'clearErrors',
			'setError'
		]),
		submitForm(){
			console.log("SUBMITTING FORM FROM PERSONAL CHANGE MODAL")
			// Save all current form fields into vuex store
			let data = this.fields
			let errors = ValidateFormSteps(this.getCurrentItem, data)
			
			if (errors["valid"] == false)
			{
				forEachValue(errors["errors"], (value, key) => {
					value.map((val) => {
						this.setError({key: key, value: value})
					})
				})
			}
			else {
				
				for (let i=0; i<data.length; i++) {
					let name = data[i].form.name;
					let value = document.getElementById(name).value
					let dest_array = data[i].dest.split('.')

					if (dest_array[1] == "address") {
						let p = dest_array[2].substring(0, dest_array[2].length - 1)
						console.log(p)
						this.setClientProp({prop: dest_array[2], data: value})
					}
					else {
						this.setClientProp({prop: dest_array[1], data: value})
					}
				}
				$('#ChangePersonalModal').modal('toggle')
			}
			console.log("errors")
			console.log(this.getErrors)

		},
	},
	computed: {
		...mapGetters([
			'getClientInfo',
			'getCart',
			'getCurrentItemProp',
			'getCurrentItem',
			'getErrors'

		]),
		checkErrors(){
			for(var e in this.getErrors){
				if(this.getErrors[e] != null){
					return true
				}
			}
			return false
		}
	}
}

</script>

<style lang="scss">

</style>