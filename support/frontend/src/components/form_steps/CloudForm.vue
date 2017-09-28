<template>
<div>
	<h2 class="text-center">{{ title }}</h2>
	<h4 class="text-center">{{ text }}</h4>

	<div v-if="this.filteredClouds.length > 0" v-show="current_step==0" id="cloud-selector-formstep" class="carousel slide" data-ride="carousel" data-interval="false" style="margin-top: 25px;">
		<!-- Indicators -->
		<!-- <ol class="carousel-indicators">
			<li v-for="(cloud, index) in getCloudProviders" data-target="#cloud-selector-formstep" :data-slide-to="index" :class="{'active': index==0}"></li>
		</ol> -->

		<!-- Wrapper for slides -->
		<div class="carousel-inner" role="listbox">
			<div v-for="(cloud, index) in filteredClouds" :class="{'item': true, 'active': cloud.pk==getCurrentCloudSelection}" :data-cloud-pk="cloud.pk">
				<img class="clickable" @click="selectProvider(index)" :src="cloud.image" style="width: auto; height: 85px;" :alt="cloud.name">
				<center><button class="btn btn-lg btn-success" @click="selectProvider(index)" style="margin-top: 20px">Select</button></center>
			</div>
			<!-- Controls -->
			<a class="left carousel-control" href="#cloud-selector-formstep" role="button" data-slide="prev">
				<span class="glyphicon glyphicon-chevron-left" aria-hidden="true" style="color: white;"></span>
				<span class="sr-only">Previous</span>
			</a>
			<a class="right carousel-control" href="#cloud-selector-formstep" role="button" data-slide="next">
				<span class="glyphicon glyphicon-chevron-right" aria-hidden="true" style="color: white;"></span>
				<span class="sr-only">Next</span>
			</a>
	    </div>

		<input type="hidden" name="cloudprovider" id="cloudprovider" :value="getCurrentCloudSelection" >

		
	</div>
		
	<div v-if="this.filteredClouds.length > 0" v-show="current_step==1" v-on:keyup.enter="chooseCloud">
		<center><img :src="filteredClouds[selected_provider].image" style="margin-top:25px; width: auto; height: 85px;" :alt="filteredClouds[selected_provider].name"></center>
		<br>
		<h4 class="text-center">{{ quantity_text }}</h4>
		<div class="container-fluid">
			<div class="col-xs-11 col-md-11">
				<label>{{fields[1].placeholder}}</label>
				<input class="form-control" type="number" :id="fields[1].form.name" :name="fields[1].form.name" v-model="cloudquantity">
				<!-- <form-text-input :step="fields[1]"></form-text-input>-->
			</div>
			<div class="col-xs-1 col-md-1" style="text-align: center;">
				<button class="btn btn-sm btn-success" style="margin: 22px 0px 0px 0px" @click="chooseCloud">Enter</button>
			</div>
		</div>
	</div>

	<div v-bind:style="buttonStyle" class="container-fluid"> 	
			<div class="col-xs-12 col-md-6" style="padding:0px;"><button v-on:keypress.enter.prevent type="button" style="width:100%;white-space: normal;" class="btn btn-lg btn-default" @click="goToLastStep">Back</button></div><div class="col-xs-12 col-md-6"  v-for="btn in buttons" style="padding:0px;"><button v-on:keypress.enter.prevent type="button" style="width:100%;white-space: normal;":class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button></div>
	</div>
</div>
</template>

<script>

import {mapGetters, mapActions} from 'vuex'
import moment from 'moment'
import axios from 'axios'

import {ValidateFormStep} from '../../scripts/functions.js'
import {forEachValue} from '../../scripts/util'

import '../../../library/carousel-swipe.js'
import FormTextInput from '../FormTextInput.vue'

export default {
	props: [
		'form',
		'buttonAction'
	],
	components: {
		FormTextInput
	},
	data() {
		return {
			quantity_text: "",
			cloudquantity: 1,
			current_step: 0,
			selected_provider: 0,
			slide_index: 0,
			fields: [
				{
					placeholder: "Cloud Provider",
					src: "cloud",
					dest: "cart.#.cloud",
					required: false,
					validate: {},
					form: {
						type: "select",
						name: "cloudprovider",
					}
				},
				{
					placeholder: "Quantity",
					src: "cloudquantity",
					dest: "cart.#.cloudquantity",
					required: true,
					validate: {
						type: "number",
						min: 1,
					},
					form: {
						type: "number",
						name: "cloudquantity",
					}
				},
			],
			buttons: [
				{

					label: "Skip",
					class: "btn btn-lg btn-success",
					script: "skip"

				},
				// {
				// 	label: "Add",
				// 	class: "btn btn-lg btn-success",

				// 	script: "addcloud"

				// },
				// {
				// 	label: "Add and Continue",
				// 	class: "btn btn-lg btn-outline-success",
				// 	script: "addcloud,next"

				// },
			],
			title: "Add Cloud Support",
			text: "Please select which cloud provider you need support for",
			error: "",
			step: 1,
			buttonStyle: "text-align: center; margin-top: 50px;"
		}
	},

	methods: {
		...mapActions([
			'setCurrentFormStep',
			'setCurrentCloudSelection',
			'setAllowFormSubmit',
			'setError',
			'checkDuplicateCloud'
		]),
		chooseCloud(){
			let key = 'cloudquantity'

			let errors = ValidateFormStep(this.fields[1], this.cloudquantity)
			if(this.cloudquantity <= 0){
				this.setError({key: key, value: ['Must be greater than 0']})
			}else{
				this.current_step = 0
				this.text = "If you need cloud support for a different provider please select below"
				let clouds = this.filteredClouds.slice(0)
				clouds.splice(this.slide_index, 1)

				let new_index = 0
				new_index = this.slide_index == this.filteredClouds.length - 1 && this.filteredClouds.length > 1 ? clouds.length - 1 : this.slide_index

				if (this.filteredClouds.length > 0) {
					this.setCurrentCloudSelection(String(clouds[new_index].pk))
				}
				this.buttonAction(null, "addcloud")
				this.slide_index = new_index
				this.selected_provider = 0
				this.cloudquantity = 1
			}

			this.buttons[0].label = "Finish Cloud"
			this.buttons[0].class = "btn btn-lg btn-success"
		},
		goToLastStep(){
			if(this.current_step > 0){
				this.current_step -= 1;
			}
			else{
				this.buttonAction(null, "back")
			}
		},
		selectProvider(index){
			let name = this.getCloudProviders[index].name
			this.setAllowFormSubmit(false)
			this.selected_provider = index
			this.current_step = 1
			this.text = ""

			if(name == 'Amazon Web Services' ||
				name == 'Google Cloud Platform' ||
				name == 'Microsoft Azure' ||
				name == 'VMware'){
				this.quantity_text = "How many instances do you have with this cloud provider?"
			}else if(name == 'Microsoft Office 365' ||
					name == 'Dynamics 365'){
				this.quantity_text = "How many users do you have on this cloud service?"
			}
			
			document.getElementById('cloudquantity').focus()
		},
		goToStep(step_num) {

			// Proceed to next page of form
			this.setCurrentFormStep(step_num)

			// Call timeout function
			// this.formTimeoutNext()

			// If step is end of client entry
			// Check server for client info
			// If not on server, create in server
			// if (step_num == this.step_names.payment) {
				// this.server_set_client()
			// }
		},
		
	},
	computed: {
		...mapGetters([
			'getCurrentCloudSelection',
			'getCloudProviders',
			'getErrors',
			'getCart',
			'filteredClouds'
		])
	},
	mounted() {
		
		// $(".carousel").swipe({
		// 	swipe: function(event, direction, distance, duration, fingerCount, fingerData)
		// 	{
		// 		if (direction == 'left') $(this).carousel('next');
		// 		if (direction == 'right') $(this).carousel('prev');
		// 	},
		// 	allowPageScroll: "vertical"
		// });
		$(".carousel").carousel({
			// percent-per-second
			// default is 50
			// false = disable touch swipe
			swipe: 30
		});

		$("#cloud-selector-formstep").bind('slid.bs.carousel', (e) => {
			console.log("carousel slide")
			this.slide_index = $('#cloud-selector-formstep .active').index('#cloud-selector-formstep .item')
			console.log("carousel index: ", this.slide_index)
			console.log(e)
			let cloud_pk = e.relatedTarget.dataset.cloudPk
			console.log(cloud_pk)
			this.setCurrentCloudSelection(cloud_pk)

		});
	}
}

</script>

<style>
	
.clickable:hover {
	cursor: pointer;
}

</style>