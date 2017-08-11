<template>
	<div id="app" class="container">
		<!-- Confirm Terms and conditions -->
		<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Terms and conditions</h4>
					</div>
					<div class="modal-body">
						Terms and conditions body.  Blah blah blah blah
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
						<button type="button" class="btn btn-primary">Accept</button>
					</div>
				</div>
			</div>
		</div>
		<!-- Price Confirmation -->
		<div class="modal fade" id="cartPriceModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Terms and conditions</h4>
					</div>
					<div class="modal-body">
						Terms and conditions body.  Blah blah blah blah
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
						<button type="button" class="btn btn-primary">Accept</button>
					</div>
				</div>
			</div>
		</div>
		<!-- PDF Quote modal -->
		<div class="modal fade" id="pdfModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Receive Estimate</h4>
					</div>
					<div class="modal-body">
						<h2>Download the PDF here:</h2>
						<p><a id="pdf-link" target="_blank" :download="'Mibura_SmartSupport_Estimate-' + new Date() + '.pdf'" :href="get_estimate_pdf">Link</a></p>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
					</div>
				</div>
			</div>
		</div>
		<!-- Call or Chat -->
		<div class="modal fade" id="chatModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Contact Sales</h4>
					</div>
					<div class="modal-body text-center">
						<h2>Cart Reference Code: {{get_cart_reference}}</h2>
					</div>
					<div class="modal-footer">
						<a type="button" href="tel:1-800-862-5144" class="btn btn-success">Call Now <i class="fa fa-phone" aria-hidden="true"></i></a>
						<button type="button" class="btn btn-info openchat">Chat Now <i class="fa fa-comment" aria-hidden="true"></i></button>
						<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
					</div>
				</div>
			</div>
		</div>
		<div v-if="get_purchase_success" class="row">
			<success-screen></success-screen>
		</div>
		<div v-else class="row">
			<div id="support-form" class="col-md-6 col-md-offset-3">
				<support-form></support-form>
			</div>
			<div id="cart" class="col-xs-12">
				<support-cart></support-cart>
			</div>
		</div>
	</div>
</template>

<script>

import SupportForm from './components/Form.vue'
import SupportCart from './components/Cart.vue'
import SuccessScreen from './components/SuccessScreen.vue'

import {mapActions,mapGetters} from 'vuex'

export default {
	name: 'app',
	data () {
		return {
		}
	},
	components: {
		SupportForm,
		SupportCart,
		SuccessScreen,
	},
	computed: {
		...mapGetters({
			get_cart_reference: 'getCartReference',
			get_purchase_success: 'getPurchaseSuccess',
			get_estimate_pdf: 'getEstimatePDF',
		})
	},
	methods: {
		...mapActions({
			'set_category_multipliers': 'setCategoryMultipliers',
		})
	},
	created() {
		this.set_category_multipliers()
	}
}
</script>

<style lang="scss">

#support-form {
	z-index: 100;
	margin-top: 5%;
}

#cart {
	margin-top: -80px;
	border-top: 1px inset #AAA;
	width: 100%;
	position: absolute;
	left: 0px;
	top: 100%;
}

</style>
