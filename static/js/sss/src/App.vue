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
		<!-- Call or Chat -->
		<div class="modal fade" id="chatModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Contact Sales</h4>
					</div>
					<div class="modal-body">
						<h2>Contact Sales</h2>
						<h2>Cart Reference Code: {{get_cart_reference}}</h2>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-info" data-dismiss="modal">Close</button>
						<button type="button" class="btn btn-primary">Accept</button>
					</div>
				</div>
			</div>
		</div>
		<div class="row">
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
	},
	computed: {
		...mapGetters({
			get_cart_reference: 'getCartReference',
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
