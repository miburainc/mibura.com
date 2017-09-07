<template>
	<div id="cloud-selector-formstep" class="carousel slide" data-ride="carousel" data-interval="false">
		<!-- Indicators -->
		<!-- <ol class="carousel-indicators">
			<li v-for="(cloud, index) in getCloudProviders" data-target="#cloud-selector-formstep" :data-slide-to="index" :class="{'active': index==0}"></li>
		</ol> -->

		<!-- Wrapper for slides -->
		<div class="carousel-inner" role="listbox">
			<div v-for="(cloud, index) in getCloudProviders" :class="{'item': true, 'active': cloud.pk==getCurrentCloudSelection}" :data-cloud-pk="cloud.pk">
				<img class="clickable" @click="addCloudItem(cloud.pk)" :src="cloud.image" style="width: auto; height: 75px;" :alt="cloud.name">
			</div>
	    </div>

	    <input type="hidden" name="cloudprovider" id="cloudprovider" :value="getCurrentCloudSelection">

		<!-- Controls -->
		<a class="left carousel-control" href="#cloud-selector-formstep" role="button" data-slide="prev">
			<span class="glyphicon glyphicon-chevron-left" aria-hidden="true" style="color: white;"></span>
			<span class="sr-only">Previous</span>
		</a>
		<a class="right carousel-control" href="#cloud-selector-formstep" role="button" data-slide="next">
			<span class="glyphicon glyphicon-chevron-right" aria-hidden="true" style="color: white;"></span>
			<span class="sr-only">Next</span>
		</a>
		<div v-bind:style="form.buttonStyle"> 	
			<button type="button" v-for="btn in form.buttons" :class="btn.class" :id="'btn_' + btn.label.toLowerCase().replace(/ /g,'_')" @click="(el) => {buttonAction(el, btn.script)}">{{btn.label}}</button>
		</div>
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
			'addCartItem',
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
	},
	computed: {
		...mapGetters([
			'getCurrentCloudSelection',
			'getCloudProviders',
			'getMultiplier',
			'getCurrentFormStep',
			'getAPIRoot',
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