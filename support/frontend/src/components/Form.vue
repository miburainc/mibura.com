<template>
	<div id="purchase-form" class="row">
		
		<form v-on:submit.prevent>
			<!-- Fade effects -->
			<transition 
				v-bind:css="false"
				v-on:before-enter="animateBeforeEnter"
				v-on:before-leave="animateBeforeLeave"
				v-on:enter="animateEnter"
				v-on:leave="animateLeave"
			>
			<div v-if="show">
			
				<h2 class="text-center">{{ get_formsteps[get_current_step].title }}</h2>
				<h4 class="text-center">{{ get_formsteps[get_current_step].text }}</h4>
				

				

				<component :is="currentComponent" :form="get_formsteps[get_current_step]"></component>

				<div v-for="(form, index) in get_formsteps" class="form-group">
					<!-- <label 
						:for="form.data.form.name"
						:style="{
							display: (form.data.form.name == 'deviceage' || form.data.form.name == 'additionalinfo') && get_current_item_prop('verified') ? 'none' : 'block'
						}"
					>

						{{ form.data.placeholder }}
					</label> -->
					<!-- Cloud -->

					<!-- <cloud-form 
						v-if="form.src && get_current_step==step_names.cloud"
						:clouds="cloud"
						:addCloudFunc="addCloudItem"
					></cloud-form> -->

					<!-- <select 
						v-else-if="data.src && get_current_step==step_names.cloud"
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
						v-else-if="get_current_step==step_names.payment"

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
							display: (data.form.name == 'deviceage' || data.form.name == 'additionalinfo') && get_current_item_prop('verified') ? 'none' : 'block'
						}"
					>

					<div class="text-red" v-for="error in get_errors[data.form.name]">
						{{ error }}
					</div>
					 -->
				</div>

			<div v-bind:style="get_formsteps[get_current_step].buttonStyle"> 	
				<button type="button" v-for="btn in get_formsteps[get_current_step].buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button>
			</div>
			<h4 v-if="form_error" class="text-red">
				{{ get_formsteps[get_current_step].error }}
			</h4>
				
			
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
// import CustomerForm from './form_steps/CustomerForm.vue'
import PaymentForm from './form_steps/PaymentForm.vue'

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
	// CustomerForm,
	PaymentForm
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
		let self = this
		function get_cloud(){
			axios.get(self.get_api_root + 'cloud')
			.then((response) => {
				self.cloud = response.data.results
			})
			.catch((error) => {
				console.error(error)
				setTimeout(get_cloud,5000)
			})
		}
		get_cloud()
	},
	methods: {
		...mapActions({
			add_cart_item: 'addCartItem',
			remove_item: 'removeCartItem',
			addProduct: 'addProduct',
			set_current_item_prop: 'setCurrentItemProp',
			set_current_form_step: 'setCurrentFormStep',
			set_error: 'setError',
			clear_errors: 'clearErrors',
			clearCurrentItem: 'clearCurrentItem',
			set_client_prop: 'setClientProp',
			add_cloud: 'addCloud',
			server_set_client: 'serverSetClient',
			add_notification: 'addNotification',
		}),

		
		logData(obj) {
			// Function for testing ajax replies
			console.log("logData")
			console.log(obj)
		},
		addCloudItem(cloud_pk) {
			let cloud = {};
			for (let i=0; i<this.cloud.length; i++) {
				if (this.cloud[i].pk == cloud_pk) {
					cloud = this.cloud[i]
				}
			}
			let cloud_obj = {
				sku: 'cloud',
				category: this.get_multiplier('cloud'),
				price_silver: cloud.price_multiplier,
				price_gold: 0.0,
				price_black: 0.0,
				type: 'cloud',
				brand: cloud.name,
				model: '',
				release: moment().format("YYYY-MM-DD"),
			}
			this.add_cart_item(cloud_obj)
				.then((value) => {
					console.log("Added cloud: ", value)
					if (value == true) {
						this.goToStep(this.get_current_step+1)
					}
				})
		},
		goToStep(step_num) {

			// Proceed to next page of form
			this.set_current_form_step(step_num)

			// Call timeout function
			this.formTimeoutNext()

			// If step is end of client entry
			// Check server for client info
			// If not on server, create in server
			if (step_num == this.step_names.payment) {
				this.server_set_client()
			}
		},
		formOnPressEnter() {

			if (this.get_current_step == this.get_formsteps[this.get_current_step].data.length - 1) {

			}
		},
		buttonAction(el, scr) {
			
			scr = scr.split(',')

			// Grab current step data
			let data = this.get_formsteps[this.get_current_step].data

			let errors = ValidateFormSteps(this.get_current_item, data)
			// If errors exist
			if(scr == "back" && this.get_current_step > 0){
				this.past_step = this.get_current_step
				this.set_current_form_step(this.get_current_step-1)
				this.formTimeoutNext()
				this.clear_errors()
			}
			if (errors["valid"] == false)
			{
				forEachValue(errors["errors"], (value, key) => {
					value.map((val) => {
						this.set_error({key: key, value: value})
					})
				})
			}
			else {
				this.clear_errors()
				for (let i=0; i<scr.length; i++) {
					switch (scr[i]) {
						case "start":
							this.past_step = this.get_current_step
							this.set_current_form_step(1)
							this.formTimeoutNext()
							break;
						case "skip":
							this.past_step = this.get_current_step
							this.set_current_form_step(this.get_current_step+1)
							this.formTimeoutNext()
							break;
						case "next":
							this.past_step = this.get_current_step

							// Save all current form fields into vuex store
							for (let i=0; i<data.length; i++) {
								let name = data[i].form.name;
								if (!this.get_current_item_prop(name)) {
									let val = document.getElementById(name).value
									this.setFormItem(val, data[i])
								}
							}

							this.goToStep(this.get_current_step+1)

							break;
						
						case "addcloud":

							let temp = document.forms.item(0).elements[0].value
							if (!temp) {
								temp = "none"
							}

							if (temp=="none") {
								temp = this.get_current_cloud_selection
							}
							this.addCloudItem(temp)

							break;
						case "review":
							this.past_step = this.get_current_step
							
							// Save all current form fields into vuex store
							for (let i=0; i<card_data.length; i++) {
								let name = card_data[i].form.name;
								if (!this.get_current_item_prop(name)) {
									let val = document.getElementById(name).value
									this.setFormItem(val, card_data[i])
								}
							}
							velocity(document.body, "scroll", { duration: 1000, mobileHA: false, offset: document.body.scrollHeight });
							
							break;
						case "additem":
							// Save all current form fields into vuex store
							for (let i=0; i<data.length; i++) {
								let name = data[i].form.name;
								if (!this.get_current_item_prop(name)) {
									let val = document.getElementById(name).value
									this.setFormItem(val, data[i])
								}
							}
							
							let model = this.get_current_item_prop('model')
							let prd = this.get_all_products
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
							this.add_cart_item(
								{
									...prd_info,
									...this.get_current_item
								}
							)
							this.clearCurrentItem()
							break;
					}
				}
			}	
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
		setItemProp () {
			this.set_current_form_step(this.get_current_step + 1)
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
					if (this.get_current_step == this.step_names.cloud) {
						this.add_notification({
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
			let transition = this.get_current_step >= this.past_step ? 'transition.slideRightIn' : 'transition.slideLeftIn'
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
			let transition = this.get_current_step > this.past_step ? 'transition.slideLeftOut' : 'transition.slideRightOut'
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
			get_product: 'getProduct',
			get_all_products: 'getAllProducts',
			get_formsteps: 'getFormSteps',
			get_current_step: 'getCurrentFormStep',
			get_current_item_prop: 'getCurrentItemProp',
			get_current_item: 'getCurrentItem',
			get_api_root: 'getAPIRoot',
			get_errors: 'getErrors',
			get_client_info: 'getClientInfo',
			get_multiplier: 'getMultiplier',
			get_current_cloud_selection: 'getCurrentCloudSelection',
		}),
		currentComponent(){
			return this.form_components[this.get_current_step]
		}
	},
	// get_api_root: 'getAPIRoot',
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

.btn-outline-success {
	padding: 10px 20px;
	color: #00a25c;
	background: transparent;
	border: 1px solid #00a25c;
	transition: 0.2s background, 0.2s color;
}

.btn-outline-success:hover {
	padding: 10px 20px;
	color: #00ec85;
	border-color: #00dc7c;
	background: transparent;
	background: rgba(0,250,144,.08);
	// border: 1px solid #FFFFFF;
}

.btn-outline-default {
	padding: 10px 20px;
	color: #8493A8;
	background: transparent;
	border: 1px solid #8493A8;
	transition: 0.2s background, 0.2s color;
}

.btn-outline-default:hover {
	padding: 10px 20px;
	color: #FFFFFF;
	background: transparent;
	background: rgba(255,255,255,.08);
	border-color: #FFFFFF;
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