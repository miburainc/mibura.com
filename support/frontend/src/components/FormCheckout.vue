<template>
	
<div>
	<h2 class="text-center">
		Checkout
	</h2>
	<div class="form-group">
		<div v-for="step in form">
			<div v-for="el in step.data">
				{{ el.form.name }}
			</div>
			
		</div>
	</div>
	<div class="button-group">
		<button class="btn btn-lg btn-default">Add product to cart</button>
		<button class="btn btn-lg btn-default">Verify ACH</button>
		<button class="btn btn-lg btn-success">Enter Estimate ID</button>
	</div>
</div>

</template>

<script>

export default {
	props: ['form'],
	mounted() {

	}
}

</script>

<style lang="scss">
	
</style>