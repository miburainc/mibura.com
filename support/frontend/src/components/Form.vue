<template>
	<div id="purchase-form" class="row">
		
		<form v-on:submit.prevent v-on:keyup.enter="formHandleEnter">
			<!-- Fade effects -->
			<transition 
				v-bind:css="false"
				v-on:before-enter="animateBeforeEnter"
				v-on:before-leave="animateBeforeLeave"
				v-on:enter="animateEnter"
				v-on:leave="animateLeave"
			>
			<div v-if="show">

				<h2 class="text-center">{{ getFormSteps[getCurrentFormStep].title }}</h2>
				<h4 class="text-center">{{ getFormSteps[getCurrentFormStep].text }}</h4>

				<!-- Dynamic component to switch between form steps -->
				<component 
					:is="currentComponent" 
					:form="getFormSteps[getCurrentFormStep]"
					:buttonAction="buttonAction" />
				
				<!--
				<div v-for="(form, index) in get_formsteps" class="form-group">
					 <label 


				<component :is="currentComponent" :form="getFormSteps[getCurrentFormStep]"></component>

				<div v-for="(form, index) in getFormSteps" class="form-group">
					<label 
						:for="form.data.form.name"
						:style="{
							display: (form.data.form.name == 'deviceage' || form.data.form.name == 'additionalinfo') && getCurrentItemProp('verified') ? 'none' : 'block'
						}"
					>

						{{ form.data.placeholder }}
					</label> -->
					<!-- Cloud -->

					<!-- <cloud-form 
						v-if="form.src && getCurrentFormStep==step_names.cloud"
						:clouds="cloud"
						:addCloudFunc="addCloudItem"
					></cloud-form> -->

					<!-- <select 
						v-else-if="data.src && getCurrentFormStep==step_names.cloud"
						:id="data.form.name"
						:name="data.form.name"
					>
						<option value="none">None</option>
						<option
							v-for="cloud in cloud"
							:value="cloud.pk"
						>
								{{cloud.name}}
						</option>
					</select> -->

					<!-- <div 
						v-else-if="getCurrentFormStep==step_names.payment"

					>
						<input type="hidden" :id="data.form.name" :name="data.form.name" hidden>
						<payment-form></payment-form>
					</div>
					<input 
					v-else
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
						:style="{
							display: (data.form.name == 'deviceage' || data.form.name == 'additionalinfo') && getCurrentItemProp('verified') ? 'none' : 'block'
						}"
					>

					<div class="text-red" v-for="error in getErrors[data.form.name]">
						{{ error }}
					</div>
					 
				</div>
				-->

			<!-- <div v-bind:style="get_formsteps[get_current_step].buttonStyle"> 	
				<button type="button" v-for="btn in get_formsteps[get_current_step].buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button>
			</div>
			<h4 v-if="form_error" class="text-red">
				{{ get_formsteps[get_current_step].error }}
			</h4> -->
				
			
			<!-- End Fade effects -->
			</div>
			</transition>	
		</form>

	</div>
</template>

<script>

// import Autocomplete from './autocomplete';


import StartForm from './form_steps/StartForm.vue'
import ProductForm from './form_steps/ProductForm.vue'
import CloudForm from './form_steps/CloudForm.vue'
import AddressForm from './form_steps/AddressForm.vue'
import ClientForm from './form_steps/ClientForm.vue'
import ReviewForm from './form_steps/ReviewForm.vue'
import PaymentForm from './form_steps/PaymentForm.vue'
import VerifyForm from './form_steps/VerifyForm.vue'
import SuccessForm from './form_steps/SuccessForm.vue'

import {mapGetters, mapActions} from 'vuex'

import moment from 'moment'
import axios from 'axios'

import Velocity from 'velocity-animate'
import 'velocity-animate/velocity.ui';

import { ValidateFormSteps } from '../scripts/functions'
import { forEachValue } from '../scripts/util'

import {step_names} from '../store/values'
import velocity from 'velocity-animate'

const form_components = [
	StartForm,
	ProductForm,
	CloudForm,
	ClientForm,
	AddressForm,
	ReviewForm,
	PaymentForm,
	VerifyForm,
	SuccessForm
]

export default {
	data () {
		return {
			show: false,
			form_data: [],
			product_info: {},
			form_error: false,
			formTransitionTime: 800,
			past_step: 0,
			step_names: step_names,
			cloud: [],
			form_components: form_components,
			componentIndex: 0
		}
	},
	mounted () {
		
	},
	methods: {
		...mapActions([
			'addCartItem',
			'addProduct',
			'saveCart',
			'setCurrentItemProp',
			'setCurrentFormStep',
			'serverGetEstimatePdf',
			'serverSetClient',
			'setError',
			'saveCart',
			'clearErrors',
			'clearCurrentItem',
			'setClientProp',
			'serverSetClient',
			'addNotification',
			'setEstimatePdfFile',
			'checkout',
			'achSendVerify',
		]),

		
		logData(obj) {
			// Function for testing ajax replies
			console.log("logData")
			console.log(obj)
		},
		
		skipToCloud() {
			this.past_step = this.getCurrentFormStep
			this.setCurrentFormStep(this.getCurrentFormStep+1)
			this.formTimeoutNext()
			this.clearErrors()
		},
		formHandleEnter(){
			let buttons = this.getFormSteps[this.getCurrentFormStep].buttons
			this.buttonAction(null, buttons[buttons.length-1].script)
		},
		addCloudItem(cloud_pk) {
			let cloud = {};
			for (let i=0; i<this.getCloudProviders.length; i++) {
				if (this.getCloudProviders[i].pk == cloud_pk) {
					cloud = this.getCloudProviders[i]
				}
			}
			let cloud_obj = {
				sku: 'cloud',
				category: this.getMultiplier('cloud'),
				price_silver: cloud.price_multiplier,
				price_gold: 0.0,
				price_black: 0.0,
				type: 'cloud',
				brand: cloud.name,
				model: '',
				release: moment().format("YYYY-MM-DD"),
			}
			this.addCartItem(cloud_obj)
				.then((value) => {
					console.log("Added cloud: ", value)
					if (value == true) {
						this.goToStep(this.getCurrentFormStep+1)
					}
				})
		},
		goToStep(step_num) {

			// Proceed to next page of form
			this.setCurrentFormStep(step_num)

			// Call timeout function
			this.formTimeoutNext()

			// If step is end of client entry
			// Check server for client info
			// If not on server, create in server
			if (step_num == this.step_names.payment) {
				this.serverSetClient()
			}
		},
		formOnPressEnter() {
			if (this.getCurrentFormStep == this.getFormSteps[this.getCurrentFormStep].data.length - 1) {

			}
		},
		buttonStartPayment() {
			velocity(document.body, "scroll", { duration: 1000, mobileHA: false, offset: 0 });
			this.setCurrentFormStep(step_names.payment)
		},
		buttonAction(el, scr) {

			console.log("button action", scr)
			scr = scr.split(',')

			// Grab current step data
			let data = this.getFormSteps[this.getCurrentFormStep].data
			this.clearErrors()
			if(scr == "submitach"){
				console.log("SubmitACH in ButtonAction")
				$('#achSubmitModal').modal('show')
				return(true)
			}
			else if(scr == "verifyach") {
				console.log("verifyACH in ButtonAction")
				this.achSendVerify()
				return(true)
			}
			else if(scr == "back" && this.getCurrentFormStep > 0){
				this.past_step = this.getCurrentFormStep
				this.setCurrentFormStep(this.getCurrentFormStep-1)
				this.formTimeoutNext()
				return(true)
			}
			else if(scr == "skip"){
				this.past_step = this.getCurrentFormStep
				this.setCurrentFormStep(this.getCurrentFormStep+1)
				this.formTimeoutNext()
				return(true)
			}
			else if(scr == "submitpayment"){
				this.past_step = this.getCurrentFormStep
				this.goToStep(this.getCurrentFormStep+1)
				return(true)
			}
			
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
				
				for (let i=0; i<scr.length; i++) {
					switch (scr[i]) {
						case "start":
							this.past_step = this.getCurrentFormStep
							this.setCurrentFormStep(1)
							this.formTimeoutNext()
							break;
						case "next":
							this.past_step = this.getCurrentFormStep

							// Save all current form fields into vuex store
							for (let i=0; i<data.length; i++) {
								let name = data[i].form.name;
								if (!this.getCurrentItemProp(name)) {
									let val = document.getElementById(name).value
									this.setFormItem(val, data[i])
								}
							}

							this.goToStep(this.getCurrentFormStep+1)

							break;
						
						case "addcloud":

							let temp = document.getElementById('cloudprovider').value

							if (temp=="none") {
								temp = this.getCurrentCloudSelection
							}
							this.addCloudItem(temp)

							break;
						case "review":
							this.past_step = this.getCurrentFormStep
							
							// Save all current form fields into vuex store
							for (let i=0; i<card_data.length; i++) {
								let name = card_data[i].form.name;
								if (!this.getCurrentItemProp(name)) {
									let val = document.getElementById(name).value
									this.setFormItem(val, card_data[i])
								}
							}
							velocity(document.body, "scroll", { duration: 1000, mobileHA: false, offset: document.body.scrollHeight });
							
							break;
						case "getquote":
							if (this.getCart.length < 1) {
								this.addNotification({
									type: 'warning',
									message: 'Please add items to your cart!'
								})
								this.buttonStartNewItem()
							}
							else if (Object.keys(this.getClientInfo).length<10) {
								this.addNotification({
									type: 'warning',
									message: 'Please provide your contact information.'
								})
								this.buttonStartClientInfo()
							}
							else {
								if (this.getCartChanged) {
									// Reset pdf to nothing
									this.setEstimatePdfFile(null);
									// Send request for new pdf file
									this.saveCart(this.getClientInfo)
										.then(() => {
											this.serverGetEstimatePdf()
										})
								}
								$('#pdfModal').modal('show')
							}
							break;
						case "additem":
							// Save all current form fields into vuex store
							for (let i=0; i<data.length; i++) {
								let name = data[i].form.name;
								if (!this.getCurrentItemProp(name)) {
									let val = document.getElementById(name).value
									this.setFormItem(val, data[i])
								}
							}
							
							let model = this.getCurrentItemProp('model')
							let prd = this.getAllProducts
							let prd_info = null;

							if (prd.hasOwnProperty(model)) {
								prd_info = prd[model]
							}
							else {
								prd_info = {
									sku: 'none',
									category: {
										category_code: 'none',
										name: 'None',
										price_multiplier: 1.0,
										yearly_tax: 0.1,
									},
									price_silver: 1.0,
									price_gold: 1.0,
									price_black: 1.0,
									type: 'product',
								}
							}
							this.addCartItem(
								{
									...prd_info,
									...this.getCurrentItem
								}
							)
							this.clearCurrentItem()
							break;
						case "purchase":
							if (this.getCart.length < 1) {
								this.addNotification({
									type: 'warning',
									message: 'Please add items to your cart before clicking purchase!'
								})
								this.buttonStartNewItem()
							}
							else if (Object.keys(this.getClientInfo) < 10) {
								this.addNotification({
									type: 'warning',
									message: 'Please fill out your information!'
								})
								this.buttonStartClientInfo()
							}
							else if (!this.getPaymentToken) {
								console.log(this.getPaymentToken)
								this.addNotification({
									type: 'warning',
									message: 'Please fill out your payment information!'
								})
								this.buttonStartPayment()
							}
							else if (!this.getAcceptedTerms) {
								this.addNotification({
									message: "Please accept terms and conditions.",
									type: "warning"})
							}
							else {
								this.serverSetClient().then(() => {
									this.saveCart().then(() => {
										this.checkout()
											.then((status) => {
												console.log("after purchase callback")
												console.log(status)
												if (status == false) {
													// Failed
													this.addNotification({
														message: "Unverified items in cart.  Please call Mibura to get your cart approved for purchase.",
														type: "danger"
													})
													this.addNotification({
														message: "To speak with Mibura about your support plan, click 'Call Sales' to speak with a Mibura sales representative.",
														type: "warning"
													})
													this.addNotification({
														message: "To revisit later, click the 'Get Quote' button in your cart to print, download, or be emailed your PDF Estimate.",
														type: "info"
													})
												}
												else{
													//finish submission of ach
													// let payload = {
													// 	'cart_ref': null,
													// 	'accountnumber': this.getPaymentInfo['accountnumber'],
													// 	'bankname': this.getPaymentInfo['bankname'],
													// 	'bankphone': this.getPaymentInfo['bankphone'],
													// 	'routingnumber': this.getPaymentInfo['routingnumber']
													// }

													console.log(this.getPaymentInfo)

													console.log("done")
												}
											})
									})
								})
								
							}
							break;
					}
				}
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
		buttonStartNewItem() {
			velocity(document.body, "scroll", { duration: 1000, mobileHA: false, offset: 0 });
			this.setCurrentFormStep(step_names.item)
		},
		buttonStartClientInfo() {
			velocity(document.body, "scroll", { duration: 1000, mobileHA: false, offset: 0 });
			this.setCurrentFormStep(step_names.client_info)
		},
		setItemProp () {
			this.setCurrentFormStep(this.getCurrentFormStep + 1)
		},
		formTimeoutNext() {
			// This method hides and shows the form to ensure smooth animations
			// It also removed old form inputs from the dom to ensure a fresh state obj each time the form changes
			// I ran into issues with input values carrying from one input to the next due to Vuejs trying to modify the dom as little as possible.
			this.show = false;
			setTimeout(() => {
				this.show = true;
				// Set another timer to ensure dom elements are loaded before calling js
				setTimeout(() => {
					document.forms[0].elements[0].focus();
					if (this.getCurrentFormStep == this.step_names.cloud) {
						this.addNotification({
							message: "If you upgrade to Gold or Black plans, you get cloud support for free!",
							type: "info"
						});
					}
				}, 100)
				
				}, 
				this.formTransitionTime
			)
		},
		animateBeforeEnter(el) {
			el.style.opacity = 0
		},
		animateBeforeLeave(el) {
			el.style.opacity = 1
		},
		animateEnter(el, done) {
			let transition = this.getCurrentFormStep >= this.past_step ? 'transition.slideRightIn' : 'transition.slideLeftIn'
			Velocity(
				el,
				transition,
				{
					duration: this.formTransitionTime,
					complete: () => {
						done()
					}
				}
			)
		},
		animateLeave(el, done) {
			let transition = this.getCurrentFormStep > this.past_step ? 'transition.slideLeftOut' : 'transition.slideRightOut'
			Velocity(
				el,
				transition,
				{
					duration: this.formTransitionTime,
					complete: () => {
						done()
					}
				}
			)
		},
		get_form_input_value(obj) {
			let dest_array = obj.dest.split('.')
			let val = ""
			if (dest_array[0] == "cart") {
				val =  this.Prop(dest_array[2])
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
			'getAllProducts',
			'getFormSteps',
			'getCurrentFormStep',
			'getCurrentItemProp',
			'getCloudProviders',
			'getMultiplier',
			'getCurrentItem',
			'getAPIRoot',
			'getErrors',
			'getClientInfo',
			'getCart',
			'getCartChanged',
			'getAcceptedTerms',
			'getPaymentToken'
		]),
		currentComponent(){
			return this.form_components[this.getCurrentFormStep]
		}
	},
	// getAPIRoot: 'getAPIRoot',
	components: {
		'cloud-form': CloudForm,
		'payment-form': PaymentForm,
		'start-form': StartForm
	},
	created () {
		setTimeout(() => this.show = true, 200)
	}
}

</script>

<style lang="scss">

@import '../assets/vue2-autocomplete';
@import '../assets/sass/form';

.startButtons{
	text-align: center;
}

.btn-outline-info {
	padding: 10px 20px;
	color: #3285C4;
	background: transparent;
	border: 1px solid #3285C4;
	transition: 0.2s background, 0.2s color;

	&:hover {
		padding: 10px 20px;
		color: #5EA4D9;
		border-color: #5EA4D9;
		background: transparent;
		background: rgba(94, 164, 217,.08);
		// border: 1px solid #FFFFFF;
	}
	&:focus {
		color: #3285C4;
	}
}

.btn-outline-danger {
	padding: 10px 20px;
	color: #ff1818;
	background: transparent;
	border: 1px solid #ff1818;
	transition: 0.2s background, 0.2s color;

	&:hover {
		padding: 10px 20px;
		color: #ff1818;
		border-color: #ff1818;
		background: transparent;
		background: rgba(255, 128, 128,.12);
	}
	&:focus {
		color: #3285C4;
	}
}

.btn-outline-success {
	padding: 10px 20px;
	color: #00a25c;
	background: transparent;
	border: 1px solid #00a25c;
	transition: 0.2s background, 0.2s color;

	&:hover {
		padding: 10px 20px;
		color: #00ec85;
		border-color: #00dc7c;
		background: transparent;
		background: rgba(0,250,144,.08);
		// border: 1px solid #FFFFFF;
	}
	&:focus {
		color: #00a25c;
	}
}

.btn-outline-default {
	padding: 10px 20px;
	color: #8493A8;	
	background: transparent;
	border: 1px solid #8493A8;
	transition: 0.2s background, 0.2s color;

	&:hover {
		padding: 10px 20px;
		color: #FFFFFF;
		background: transparent;
		background: rgba(255,255,255,.08);
		border-color: #FFFFFF;
	}

	&:focus {
		color: #8493A8;
	}
}
.btn:active, .btn:visited, .btn:focus {
	outline: none !important;
}

.form-input-wrapper {
	width: 100%;
}

label {
	color: #DADADA;
	margin-bottom: 0;
}

.label-disabled{
	color: #545454!important; 
}

input[type=text], select, .form-control {
	background: transparent;
	color: white;
    width: 100%;
    padding: 12px 20px;
    margin: 2px 0 8px 0;
    display: inline-block;
    border: 1px solid #8493A8;
    border-radius: 4px;
    box-sizing: border-box;

    &:disabled {
		background: transparent;
		color: #545454!important;
		cursor: initial!important;
		border: 1px solid #545454!important;
	}
}

.form-input-list {
    ul {
    	margin-left: 22%;
    	width: 50%;
    	li {
    		// width: 100%;
    		a {
    			// padding: 0;
    		}
    	}
    }
}

.text-red {
	color: red;
}

/* Enter and leave animations can use different */
/* durations and timing functions.              */
.slide-fade-enter-active {
  transition: all .5s ease;
}
.slide-fade-leave-active {
  transition: all .5s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-enter
/* .slide-fade-leave-active for <2.1.8 */ {
  transform: translateX(30px);
  opacity: 0;
}
.slide-fade-leave-to
/* .slide-fade-leave-active for <2.1.8 */ {
  transform: translateX(-30px);
  opacity: 0;
}

// Stripe

.field {
	background: transparent;
	box-sizing: border-box;
	font-weight: 400;
	border: 1px solid #8493A8;
	border-radius: 4px;
	color: #ffffff;
	outline: none;
	height: 48px;
	line-height: 48px;
	padding: 0 20px;
	cursor: text;
	width: 100%;
}

.field:focus,
.field.StripeElement--focus {
  border-color: #F99A52;
}

.outcome {
  float: left;
  width: 100%;
  padding-top: 8px;
  min-height: 20px;
  text-align: center;
}

.success, .error {
  display: none;
  font-size: 13px;
}

.success.visible, .error.visible {
  display: inline;
}

.error {
  color: #E4584C;
}

.success {
  color: #F8B563;
}

.success .token {
  font-weight: 500;
  font-size: 13px;
}

</style>