<template>
	
<div>
	<div class="form-group" >

		<div ref="input" v-for="(step, index) in form.data" 
			:style="{
					display: ((step.form.name == 'deviceage' || step.form.name == 'additionalinfo') && getCurrentItemProp('verified') == true) ? 'none' : 'block'
				}">
			
			<label>{{ step.placeholder }}</label>
			<input 
				@keyup.enter.prevent="formHandleEnter(index)"
				:data-index="index"
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
			<div class="text-red" v-for="error in getErrors[step.form.name]">
				{{ error }}
			</div>

		</div>
		<div v-bind:style="form.buttonStyle"> 	
			<button type="button" v-for="btn in form.buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button>
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

	},
	methods: {
		...mapActions([
			'setCurrentItemProp',
			'setClientProp'
		]),
		formHandleEnter(index) {
			
			if(index < this.$refs.input.length){
				console.log(this.$refs)
				console.log(index)
				this.$refs.input[index+1].children[1].focus();	
			}
			else{
				//PUT BUTTON ACTION
				console.log("Button Action Here--")
			}
			
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