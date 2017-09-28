<template>
	<div v-on:keyup.enter="submitForm" class="modal" id="UnverifiedItemsModal" tabindex="1" role="dialog" aria-labelledby="myModalLabel">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
					<h4 class="modal-title" id="myModalLabel">Unverified Items</h4>
				</div>
				<div class="modal-body">
					<p>{{ getUnverifiedItems.length }} unverified items in your cart.</p>
					<div v-for="item in getUnverifiedItems"><p>&nbsp;&nbsp;&nbsp;-&nbsp;{{ item.model }}</p></div> 
					<br><p>You will not be able to checkout with these items.</p>
					<p>If you would like to submit your cart for verification we will reach out to you within the next business day to help complete your order.</p>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
					<button type="button" class="btn btn-primary" @click="submitForm">Submit Cart for Verification</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

import {mapGetters, mapActions} from 'vuex'

import { ValidateFormSteps } from '../scripts/functions'
import { forEachValue } from '../scripts/util'
import { step_names } from '../store/values'

import FormTextInput from '../components/FormTextInput.vue'

export default {
	props: ['buttonAction'],
	components:{
	},
	data() {
		return {
		}
	},
	mounted() {

	},
	methods: {
		...mapActions([
			'setClientProp',
			'clearError',
			'clearErrors',
			'setError',
			'setCurrentFormStep',
			'serverSetClient',
			'saveCart',
			'setPurchaseSuccess',
			'setCartStatus'
		]),
		submitForm(){
			this.setCartStatus("awaiting_product_approval")
			this.serverSetClient()
			.then(() => {
				this.saveCart()
			})
			$('#UnverifiedItemsModal').modal("toggle")
			this.setPurchaseSuccess(true)
		},
	},
	computed: {
		...mapGetters([
			'getClientInfo',
			'getCart',
			'getCurrentItemProp',
			'getCurrentItem',
			'getUnverifiedItems'
		])
	}
}

</script>

<style lang="scss">

</style>