<template>
	<div id="app" class="container">
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

export default {
  name: 'app',
  data () {
    return {
    }
  },
  components: {
    SupportForm,
    SupportCart,
  }
}
</script>

<style lang="scss">

#support-form {
	z-index: 100;
	margin-top: 5%;
}

#cart {
	margin-top: -77px;
	border-top: 1px inset #AAA;
	width: 100%;
	position: absolute;
	left: 0px;
	top: 100%;
	height: 400px;
}

</style>
