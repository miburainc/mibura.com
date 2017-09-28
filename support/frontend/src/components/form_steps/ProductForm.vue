<template>
	
<div>
	<h2 class="text-center">{{ title }}</h2>
	<h4 class="text-center">{{ text }}</h4>
	<div class="form-group" v-on:keyup.enter="submitForm"> 

		<label>Product Name</label> &nbsp;&nbsp;&nbsp;&nbsp;<label class="text-red" v-if="getErrors[form.data[0].form.name]"> {{ getErrors[fields[0].form.name][0] }}</label>
		<autocomplete
			:style="{borderColor: (getErrors[fields[0].form.name] ? 'red' : '#8493A8')}"
			:url="getAPIRoot + 'productcomplete/'"
			data-root="results"
			label="brand"
			anchor="model"
			param="s"
			:class="{'autocomplete-border': getErrors[form.data[0].form.name]}"
			class-name="form-input"
			:custom-params="{format: 'json'}"
			:name="fields[0].form.name"
			:id="fields[0].form.name"
			:init-value="getCurrentItemProp(fields[0].form.name)"
			:process="processAjaxResult"
			:placeholder="fields[0].placeholder"
			:on-select="(obj) => {setFormItemAutoselect(obj, fields[0].form.name);}"
			:min="2"
			:onInput="(el) => {
				resetVerified()
				ValidateFormStepFunction(fields[0], el)
			}"
			style="position:relative; z-index:1;">
		</autocomplete>

		<div ref="input" v-for="(step, index) in fields" v-if="index > 0" 
			:style="{
					display: ((step.form.name == 'deviceage' || step.form.name == 'additionalinfo') && getCurrentItemProp('verified') == true) ? 'none' : 'block'
				}">
			
			<form-text-input :step="step"></form-text-input>
			
		</div>
		<div v-bind:style="form.buttonStyle" class="container-fluid" style="padding:0px;"> 	
			<div class="col-xs-12 col-md-2 btn-container">
				<button type="button" v-on:keypress.enter.prevent :class="buttons[0].class" :id="'btn_' + buttons[0].label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, buttons[0].script)}">{{form.buttons[0].label}}</button>
			</div>
			<div class="col-xs-12 col-md-2 btn-container">
				<button type="button" v-on:keypress.enter.prevent :class="buttons[1].class" :id="'btn_' + buttons[1].label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, buttons[1].script)}">{{form.buttons[1].label}}</button>
			</div>
			<div class="col-xs-12 col-md-4 btn-container">
				<button type="button" v-on:keypress.enter.prevent :class="buttons[2].class" :id="'btn_' + buttons[2].label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, buttons[2].script)}">
						{{form.buttons[2].label}}
				</button>
			</div>
			<div v-if="getCart.length > 0" class="col-xs-12 col-md-4 btn-container">
				<button type="button" v-on:keypress.enter.prevent class="btn btn-lg btn-info" @click="buttonAction(null, 'skip')">
					Skip to Cloud
				</button>
			</div>

		</div>
	</div>
</div>

</template>

<script>

import {mapGetters, mapActions} from 'vuex'

import { ValidateFormStep } from '../../scripts/functions'

import Autocomplete from 'vue2-autocomplete-js';
import FormTextInput from '../FormTextInput.vue'

export default {
	props: ['form', 'buttonAction'],
	components:{
		Autocomplete,
		FormTextInput
	},
	data() {
		return {
			title: "On-Premise Hardware - Software",
			text: "Search for your hardware device or software below",
			canSubmit: true,
			fields: [
				{
					placeholder: "Product Name",
					dest: "cart.#.brand",
					required: true,
					form: {
						type: "text",
						name: "model",
					},
					validate: {
						type: "text",
						min: 2,
					}
				},
				{
					placeholder: "Serial Number",
					dest: "cart.#.sn",
					required: true,
					form: {
						type: "text",
						name: "serialnumber"
					},
					validate: {
						min: 3
					},
				},
				{
					placeholder: "Device Age (Years)",
					dest: "cart.#.age",
					required: false,
					form: {
						type: "number",
						name: "deviceage",
					},
					validate: {}
				},
				{
					placeholder: "Additional Info",
					dest: "cart.#.info",
					required: false,
					validate: {},
					form: {
						name: "additionalinfo",
						type: "textarea"
					}
				}
			],buttons: [
				{
					label: "Back",
					class: "btn btn-lg btn-default",
					script: "back"
				},
				{
					label: "Add",
					class: "btn btn-lg btn-success",
					script: "start,additem"

				},
				{
					label: "Add and Continue",
					class: "btn btn-lg btn-success",
					script: "next,additem"

				},
			],
		}
	},
	mounted() {

	},
	methods: {
		...mapActions([
			'setCurrentItemProp',
			'setClientProp',
			'clearError',
			'clearErrors',
			'setAllowFormSubmit'
		]),
		submitForm(){
			if(!this.canSubmit){
				document.getElementById(this.fields[1].form.name).focus()
				this.canSubmit = true
			}
			else{
				this.buttonAction(null, "next,additem")
			}
		},
		processAjaxResult(json) {
			return json['results']
		},
		test(el){
			console.log(el)
		},
		ValidateFormStepFunction(step, value){
			//let s = step.dest.split('.')
			//this.setCurrentItemProp({prop: s[s.length-1], data: value})
			let errors = ValidateFormStep(step, value)

			if(errors['valid'] == true){
				this.clearError(step.form.name)
			}
		},
		setFormItemAutoselect (obj, name) {
			this.canSubmit = false
			for(var key in obj){
				if(obj.hasOwnProperty(key)){
					this.setCurrentItemProp({prop:key, data:obj[key]})	
				}
			}
			this.setCurrentItemProp({ prop: 'verified', data: true })

			this.setAllowFormSubmit(false)
			setTimeout(() => {this.setAllowFormSubmit(true)}, 200)
			document.getElementById('serialnumber').focus()
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
			'getAPIRoot',
			'getErrors',
			'getCart'
		])
	}
}

</script>

<style lang="scss">

label {
	color: #333;
}

.btn-container {
	padding: 0px;
	margin: 0px;
	button {
		white-space: normal;
		width: 100%;
	}
}

.autocomplete-border > input {
	border-color: #ff3434;

	&:focus {
		border-color: red;
    -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 8px rgba(255, 52, 52, 0.6);
    box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 8px rgba(255, 52, 52, 0.6);
    	outline: none;
	}
}

.btn-outline-info {
	padding: 10px 20px;
	color: #3285C4;
	background: transparent;
	border: 1px solid #3285C4;
	transition: 0.2s background, 0.2s color;
}

.btn-outline-info:hover {
	padding: 10px 20px;
	color: #5EA4D9;
	border-color: #5EA4D9;
	background: transparent;
	background: rgba(94, 164, 217,.08);
	// border: 1px solid #FFFFFF;
}


	
</style>