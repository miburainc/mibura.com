<template>
	<div class="row">

		<div class="col-xs-12 text-center">
			<h1>Success!</h1>
		</div>
		<div style="background: white;" class="col-xs-10 col-xs-offset-1 col-md-6 col-md-offset-3 text-center">
			<h3>{{ getPlan(getCurrentPlan).name }}</h3>
			<h4>Cart Reference Code: {{ getCartReference }}</h4>
			<table class="table table-hover table-striped">
				<thead>
					<th>Brand</th>
					<th>Model</th>
					<th>Price</th>
				</thead>
				<tbody>
					<tr v-for="(item, index) in getCart">
						<td>{{ item.brand }}</td>
						<td>{{ item.model }}</td>
						<td>${{ numWithCommas(getProductSubtotal(index)-getProductSubtotal(index)*getCurrentDiscount) }}</td>
					</tr>
				</tbody>
			</table>
			<p>
			SubTotal: ${{ numWithCommas(getTotal) }}<br>
				%{{getCurrentDiscount*100}} Discount: &nbsp;
				- ${{numWithCommas(getTotal*getCurrentDiscount)}}<br>
				<span style="font-size: 1.2em;font-weight:700;">Payment Total: ${{ numWithCommas(getGrandTotal) }}</span>
			</p>
		</div>
	</div>
</template>

<script>

import { mapGetters, mapActions } from 'vuex'

export default {
	computed: {
		...mapGetters([
			'numWithCommas',
			'getPlan',
			'getCurrentPlan',
			'getCart',
			'getCartReference',

			'getProductSubtotal',
			'getTotal',
			'getGrandTotal',
			'getCurrentDiscount',
		])
	},
	methods: {
		...mapActions([
			
		])
	}
}

</script>

<style scoped>

div h1 {
	color: white;
}

</style>