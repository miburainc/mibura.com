<template>
	
<div>
	<div class="form-group"> 

		<label>Product Name</label> &nbsp;&nbsp;&nbsp;&nbsp;<label class="text-red" v-if="getErrors[form.data[0].form.name]"> {{ getErrors[form.data[0].form.name][0] }}</label>
		<autocomplete
			:style="{borderColor: (getErrors[form.data[0].form.name] ? 'red' : '#8493A8')}"
			:url="getAPIRoot + 'productcomplete'"
			data-root="results"
			label="brand"
			anchor="model"
			param="s"
			:class="{'autocomplete-border': getErrors[form.data[0].form.name]}"
			class-name="form-input"
			:custom-params="{format: 'json'}"
			:name="form.data[0].form.name"
			:id="form.data[0].form.name"
			:init-value="getCurrentItemProp(form.data[0].form.name)"
			:process="processAjaxResult"
			:placeholder="form.data[0].placeholder"
			:on-select="(obj) => {setFormItemAutoselect(obj, form.data[0].form.name);}"
			:min="2"
			:onInput="(el) => {
				resetVerified()
				ValidateFormStepFunction(form.data[0], el)

			}">
		</autocomplete>
		<!-- <autocomplete
            v-if=“data.src && get_current_step==step_names.brand”
            :url=“getAPIRoot + ‘productcomplete’”
            label=“brand”
            anchor=“model”
            param=“s”
            class-name=“form-input”
            :custom-params=“{format: ‘json’}”
            :name=“data.form.name”
            :id=“data.form.name”
            :init-value=“getCurrentItemProp(data.form.name)”
            :process=“processAjaxResult”
            :on-ajax-loaded=“logData”
            :placeholder=“data.placeholder”
            :on-select=“(obj) => { setFormItemAutoselect(obj, data.form.name);
                buttonAction(obj, ‘next’); }”
            :min=“2”>
        </autocomplete> -->

		<div ref="input" v-for="(step, index) in form.data" v-if="index > 0" 
			:style="{
					display: ((step.form.name == 'deviceage' || step.form.name == 'additionalinfo') && getCurrentItemProp('verified') == true) ? 'none' : 'block'
				}">
			
			<form-text-input :step="step"></form-text-input>

			


			
		</div>
		<div v-bind:style="form.buttonStyle"> 	
			<button style="margin-right:3px" v-on:keypress.enter.prevent type="button" v-for="btn in form.buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button><button v-on:keypress.enter.prevent v-if="getCart.length" class="btn btn-lg btn-outline-info" type="button" @click="buttonAction(null, 'skip')">Skip to Cloud Services</button>

		</div>
	</div>
	<!-- div class="button-group">
		<button class="btn btn-lg btn-success">Add product to cart</button>
		<button class="btn btn-lg btn-info">Verify ACH</button>

		<button type="button" class="btn btn-lg btn-primary" @click="buttonGetEstimate"><i class="fa fa-upload" aria-hidden="true"></i> Enter Estimate ID</button>
	</div> -->
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
	mounted() {

	},
	methods: {
		...mapActions([
			'setCurrentItemProp',
			'setClientProp',
			'clearError'
		]),
		processAjaxResult(json) {
			return json['results']
		},
		test(el){
			console.log(el)
		},
		ValidateFormStepFunction(step, value){
			let s = step.dest.split('.')
			this.setCurrentItemProp({prop: s[s.length-1], data: value})
			let errors = ValidateFormStep(step, value)

			if(errors['valid'] == true){
				this.clearError(step.form.name)
			}
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
			'getAPIRoot',
			'getErrors',
			'getCart'
		])
		
	}
}

</script>

<style lang="scss">

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