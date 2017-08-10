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
				
				<div v-for="data in get_formsteps[get_current_step].data" class="form-group">
					<label :for="data.form.name">{{ data.placeholder }}</label>
					<!-- brand -->
					<autocomplete
						v-if="data.src && get_current_step==step_names.brand"
						:url="get_api_root + 'productcomplete'"
						data-root="results"
						anchor="brand"
						param="brand"
						class-name="form-input"
						:custom-params="{format: 'json'}"
						:name="data.form.name"
						:id="data.form.name"
						:init-value="get_current_item_prop(data.form.name)"
						:on-ajax-loaded="logData"
						:placeholder="data.placeholder"
						:on-select="(obj) => { setFormItemAutoselect(obj, data.form.name);
							buttonAction(obj, 'next'); }"
						:min="2">
					</autocomplete>
					<!-- model -->
					<autocomplete
						v-else-if="data.src && get_current_step==1"
						:url="get_api_root + 'productcomplete'"
						anchor="model"
						data-root="results"
						param="model"
						class-name="form-input"
						:custom-params="{brand: get_current_item_prop('brand'), format: 'json'}"
						:name="data.form.name"
						:id="data.form.name"
						:init-value="get_current_item_prop(data.form.name)"
						:placeholder="data.placeholder"
						:on-select="(obj) => { setFormItemAutoselect(obj, data.form.name);
							buttonAction(obj, 'next'); }"
						:min="2">
					</autocomplete>
					<!-- Cloud -->
					<select 
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
					</select>
					<div v-else-if="data.form.type=='stripe'">
						<div id="card-element" class="field"></div>
						<div class="outcome">
							<div class="error" role="alert"></div>
<!-- 							<div class="success">
								Success! Your Stripe token is <span class="token"></span>
							</div> -->
						</div>
					</div>
					<input 
					autofocus
					v-else 
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

					<div class="text-red" v-for="error in get_errors[data.form.name]">
						{{ error }}
					</div>
				</div>

			<button type="button" v-for="btn in get_formsteps[get_current_step].buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button>
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

import Autocomplete from 'vue2-autocomplete-js';

import {mapGetters, mapActions} from 'vuex'

import moment from 'moment'
import axios from 'axios'

import Velocity from 'velocity-animate'
import 'velocity-animate/velocity.ui';

import { ValidateFormSteps } from '../scripts/functions'
import { forEachValue } from '../scripts/util'

import {step_names} from '../store/values'
import velocity from 'velocity-animate'

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
		}
	},
	mounted () {
		console.log(this.get_api_root)
		console.log("Created()")
		axios.get(this.get_api_root + 'cloud')
			.then((response) => {
				console.log(response.data.results)
				this.cloud = response.data.results
			})
			.catch((error) => {
				console.error(error)
			})
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
			set_payment_token: 'setPaymentToken',
			add_cloud: 'addCloud',
			serverSetClient: 'serverSetClient',
		}),
		logData(obj) {	// Function for testing ajax replies
			console.log("logData")
			console.log(obj)
		},
		buttonAction(el, scr) {
			let temp = document.forms.item(0).elements[0].value
			scr = scr.split(',')
			for (let i=0; i<scr.length; i++) {
				switch (scr[i]) {
					case "start":
						this.past_step = this.get_current_step
						this.set_current_form_step(0)
						this.formTimeoutNext()
						break;
					case "skip":
						this.set_current_form_step(this.get_current_step+1)
						this.formTimeoutNext()
						break;
					case "next":

						// If step is end of client entry
						// Check server for client info
						// If not on server, create in server
						if (this.get_current_step == this.step_names.client_address) {
							this.serverSetClient()
						}

						this.past_step = this.get_current_step
						let data = this.get_formsteps[this.get_current_step].data
						
						for (let i=0; i<this.get_formsteps[this.get_current_step].data.length; i++) {
							let formstep = this.get_formsteps[this.get_current_step].data;
							let name = formstep[i].form.name;
							if (!this.get_current_item_prop(name)) {
								let val = document.getElementById(name).value
								this.setFormItem(val, formstep[i])
							}
						}

						this.clear_errors()
						let errors = ValidateFormSteps(this.get_current_item, data)
						if (errors["valid"] == false)
						{
							forEachValue(errors["errors"], (value, key) => {
								value.map((val) => {
									this.set_error({key: key, value: value})
								})
							})
							
							break;
						}
						else {
							this.clear_errors()
							this.set_current_form_step(this.get_current_step+1)
						}
						this.formTimeoutNext()

						

						break;
					case "back":
						this.past_step = this.get_current_step
						this.set_current_form_step(this.get_current_step-1)
						this.formTimeoutNext()
						break;
					case "addcloud":
						if (temp=="none") {
							break;
						}
						let cloud = {};
						for (let i=0; i<this.cloud.length; i++) {
							if (this.cloud[i].pk == temp) {
								cloud = this.cloud[i]
							}
						}
						console.log(cloud)
						let cloud_obj = {
								sku: 'none',
								category: this.get_multiplier('cloud'),
								price_silver: 1,
								price_gold: 1,
								price_black: 1,
								with_cloud: 1,
								type: 'cloud',
								brand: cloud.name,
								model: '',
								release: moment().format("YYYY-MM-DD"),
							}
						this.add_cart_item(cloud_obj)
						break;
					case "review":
						velocity(document.body, "scroll", { duration: 1000, mobileHA: false, offset: document.body.scrollHeight });
						break;
					case "additem":
						let model = this.get_current_item_prop('model')
						let prd = this.get_all_products
						let prd_info = null;

						if (prd.hasOwnProperty(model)) {
							prd_info = prd[model]
						}
						else {
							prd_info = {
								sku: 'none',
								category: 'none',
								price_silver: 1,
								price_gold: 1,
								price_black: 1,
								with_cloud: 1,
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
				
		},
		setFormItemAutoselect (obj, name) {
			console.log("Name: " + name)
			console.log("Obj: ", obj)
			this.set_current_item_prop({ prop: name, data: obj[name] })

			if (name == "model") {
				this.addProduct({id: obj.model, data: obj})
				// this.$set(this.product_info, obj['model'], obj)
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
		},
		setItemProp () {
			console.log("setItemProp ------")			
			this.set_current_form_step(this.get_current_step + 1)
		},
		formTimeoutNext() {
			this.show = false;
			setTimeout(() => {
				this.show = true;
				setTimeout(() => {
					document.forms[0].elements[0].focus();
					if (this.get_current_step==this.step_names.payment) {
						var stripe = Stripe('pk_test_8TjNbehh0cqmd01HFq3DIawx');
						var elements = stripe.elements();
						var card = elements.create('card', {
							style: {
								base: {
									iconColor: '#eca661',
									color: '#ffffff',
									lineHeight: '40px',
									fontWeight: 300,
									fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
									fontSize: '15px',

									'::placeholder': {
										color: '#CFD7E0',
									},
								},
							}
						});
						card.mount('#card-element');
						var self = this;
						function setOutcome(result) {
							var errorElement = document.querySelector('.error');
							errorElement.classList.remove('visible');
							if (result.token) {
								// Use the token to create a charge or a customer
								// https://stripe.com/docs/charges
								self.set_payment_token(result.token.id);
							} else if (result.error) {
								errorElement.textContent = result.error.message;
								errorElement.classList.add('visible');
							}
						}
						card.on('change', function(event) {
							setOutcome(event);
						});
						document.querySelector('#btn_review').addEventListener('click', function(e) {
							e.preventDefault();
							var form = document.querySelector('form');
							var extraDetails = {
								name: form.querySelector('input[name=cardholder-name]').value,
							};
							stripe.createToken(card, extraDetails).then(setOutcome);
						});
					}
				}, 100)
				
				}, 
				this.formTransitionTime)
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
		}
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
		}),
	},
	// get_api_root: 'getAPIRoot',
	components: {
		Autocomplete
	},
	created () {
		setTimeout(() => this.show = true, 200)
	}
}

</script>

<style lang="scss">

@import '../assets/vue2-autocomplete';
@import '../assets/sass/form';

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