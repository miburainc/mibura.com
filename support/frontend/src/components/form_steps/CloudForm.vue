<template>
	<div id="cloud-selector-formstep" class="carousel slide" data-ride="carousel" data-interval="false" style="margin-top: 25px;">
		<!-- Indicators -->
		<!-- <ol class="carousel-indicators">
			<li v-for="(cloud, index) in getCloudProviders" data-target="#cloud-selector-formstep" :data-slide-to="index" :class="{'active': index==0}"></li>
		</ol> -->

		<!-- Wrapper for slides -->
		<div class="carousel-inner" role="listbox">
			<div v-for="(cloud, index) in getCloudProviders" :class="{'item': true, 'active': cloud.pk==getCurrentCloudSelection}" :data-cloud-pk="cloud.pk">
				<img class="clickable" @click="(el) => {buttonAction(el, 'addcloud')}" :src="cloud.image" style="width: auto; height: 85px;" :alt="cloud.name">
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

		<div v-bind:style="form.buttonStyle" class="btn-2-round"> 	
			<button v-on:keypress.enter.prevent type="button" v-for="btn in form.buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button>
		</div>
		<input type="hidden" name="cloudprovider" id="cloudprovider" :value="getCurrentCloudSelection" >
	</div>
	
</template>

<script>

import {mapGetters, mapActions} from 'vuex'
import moment from 'moment'
import axios from 'axios'

import '../../../library/carousel-swipe.js'

export default {
	props: [
		'form',
		'buttonAction'
	],
	data() {
		return {
			selected_cloud: -1,
		}
	},

	methods: {
		...mapActions([
			'setCurrentFormStep',
			'setCurrentCloudSelection',
			
		]),
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
			let cloud_pk = e.relatedTarget.dataset.cloudPk
			// console.log(cloud_pk)
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