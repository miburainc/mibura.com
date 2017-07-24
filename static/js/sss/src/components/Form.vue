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
			
				<h2 class="text-center">{{ formsteps[current_step].title }}</h2>
				<h4 class="text-center">{{ formsteps[current_step].text }}</h4>
				
				<div v-for="data in formsteps[current_step].data" class="form-group">
					<label :for="data.form.name">{{ data.placeholder }}</label>
					<!-- brand -->
					<autocomplete
						v-if="data.src && current_step==0"
						:url="get_api_root + '/productcomplete'"
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
						:on-blur="setFormItem"
						:on-select="(obj) => { setFormItemAutoselect(obj, data.form.name) }"
						:min="2">
					</autocomplete>
					<!-- model -->
					<autocomplete
						v-else-if="data.src && current_step==1"
						:url="get_api_root + '/productcomplete'"
						anchor="model"
						data-root="results"
						param="model"
						class-name="form-input"
						:custom-params="{brand: get_current_item_prop('brand'), format: 'json'}"
						:name="data.form.name"
						:id="data.form.name"
						:init-value="get_current_item_prop(data.form.name)"
						:placeholder="data.placeholder"
						:on-blur="setFormItem"
						:on-select="(obj) => { setFormItemAutoselect(obj, data.form.name) }"
						:min="2">
					</autocomplete>
					<!-- Cloud -->
					<autocomplete
						v-else-if="data.src && current_step==3"
						:url="get_api_root + '/cloud'"
						anchor="name"
						data-root="results"
						param="cloud"
						class-name="form-input"
						:custom-params="{format: 'json'}"
						:name="data.form.name"
						:id="data.form.name"
						:init-value="get_current_item_prop(data.form.name)"
						:placeholder="data.placeholder"
						:on-blur="setFormItem"
						:on-ajax-loaded="logData"
						:on-select="(obj) => { setFormItemAutoselect(obj, data.form.name) }"
						:min="2">
					</autocomplete>
					<input 
					autofocus
					v-else 
						:type="data.type" 
						:id="data.form.name" 
						:name="data.form.name" 
						:placeholder="data.placeholder" 
						class="form-control" 
						:value="get_current_item_prop(data.form.name)" 
						@change="setFormItem"
					>
					<div class="text-red" v-for="error in get_errors[data.form.name]">
						{{ error }}
					</div>
				</div>

			<button type="button" v-for="btn in formsteps[current_step].buttons" :class="btn.class" @click="buttonAction(this, btn.script)">{{btn.label}}</button>
			<h4 v-if="form_error" class="text-red">
				{{ formsteps[current_step].error }}
			</h4>
			
			<!-- Fade effects -->
			</div>
			</transition>	
		</form>
	</div>
</template>

<script>

import Autocomplete from 'vue2-autocomplete-js';

import {mapGetters, mapActions} from 'vuex'

import Velocity from 'velocity-animate'
import 'velocity-animate/velocity.ui';

import { ValidateFormSteps } from '../scripts/functions'
import { forEachValue } from '../scripts/util'

export default {
	data () {
		return {
			show: false,
			form_data: [],
			product_info: {},
			form_error: false,
			formTransitionTime: 800,
			past_step: 0,

		}
	},
	methods: {
		...mapActions({
			add_item: 'addCartItem',
			remove_item: 'removeCartItem',
			set_current_item_prop: 'setCurrentItemProp',
			set_current_form_step: 'setCurrentFormStep',
			set_error: 'setError',
			clear_errors: 'clearErrors',
		}),
		logData(obj) {	// Function for testing ajax replies
			console.log("logData")
			console.log(obj)
		},
		buttonAction(el, scr) {
			let temp = document.getElementById(this.formsteps[this.current_step].data[0].form.name).value
			scr = scr.split(',')
			for (let i=0; i<scr.length; i++) {
				switch (scr[i]) {
					case "start":
						this.past_step = this.current_step
						this.set_current_form_step(0)
						this.formTimeoutNext()
						break;
					case "next":
						this.past_step = this.current_step
						let data = this.formsteps[this.current_step].data
						let errors = ValidateFormSteps(this.get_current_item, data)
						if (errors["valid"] == false)
						{

							forEachValue(errors["errors"], (value, key) => {
								console.log(key)
								value.map((val) => {
									this.set_error({key: key, value: value})
								})
							})
							
							break;
						}
						else {
							this.clear_errors()
							this.set_current_form_step(this.current_step+1)
						}
						this.formTimeoutNext()
						break;
					case "back":
						this.past_step = this.current_step
						this.set_current_form_step(this.current_step-1)
						this.formTimeoutNext()
						break;
					case "additem":
						this.add_item(this.product_info[this.get_current_item_prop('model')])
						break;
				}
			}
				
		},
		setFormItemAutoselect (obj, name) {
			console.log("Name: "+name)
			console.log("Obj: "+obj)
			this.set_current_item_prop({prop: name, data: obj[name]})

			if (name == "model") {
				this.$set(this.product_info, obj['model'], obj)
			}
		},
		setFormItem (el) {
			let name = el.target.id
			let value = el.target.value
			// this.$set(this.form_data, name, value)
			this.set_current_item_prop({prop: name, data: value})
		},
		setItemProp () {
			console.log("setItemProp ------")			
			this.set_current_form_step(this.current_step + 1)
		},
		formTimeoutNext() {
			this.show = false;
			setTimeout(() => this.show = true, this.formTransitionTime)
		},
		animateBeforeEnter(el) {
			el.style.opacity = 0
		},
		animateBeforeLeave(el) {
			el.style.opacity = 1
		},
		animateEnter(el, done) {
			let transition = this.current_step >= this.past_step ? 'transition.slideRightIn' : 'transition.slideLeftIn'
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
			let transition = this.current_step > this.past_step ? 'transition.slideLeftOut' : 'transition.slideRightOut'
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
		}
	},
	computed: {
		...mapGetters({
			formsteps: 'getFormSteps',
			current_step: 'getCurrentFormStep',
			get_current_item_prop: 'getCurrentItemProp',
			get_current_item: 'getCurrentItem',
			get_api_root: 'getAPIRoot',
			get_errors: 'getErrors',
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

.btn-success {
	padding: 10px 20px;
	color: #04BE5B;
	background: transparent;
	border: 1px solid #04BE5B;
	transition: 0.2s background, 0.2s color;
}

.btn-success:hover {
	padding: 10px 20px;
	color: #FFFFFF;
	background: transparent;
	// border: 1px solid #FFFFFF;
}

.btn-default {
	padding: 10px 20px;
	color: #8493A8;
	background: transparent;
	border: 1px solid #8493A8;
	transition: 0.2s background, 0.2s color;
}

.btn-default:hover {
	padding: 10px 20px;
	color: #FFFFFF;
	background: rgba(0,0,0,.01);
	border: 1px solid #FFFFFF;
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



</style>