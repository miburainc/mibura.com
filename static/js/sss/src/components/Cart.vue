<template>

<div id="sss-cart">
	<div class="row" :style="{'background-color': plans[current_plan].color, 'color': current_plan == 2 ? 'white' : 'black' }">
		<div class="col-xs-6 col-md-4">
			<h2 class="cart-tray" :style="textColorPlan">${{ getTotal }} / yr</h2>
		</div>
		<div class="col-md-4">
			<div class="text-center" :style="textColorPlan">Plan
			<div class="form-group">
				<select class="form-control" v-model="current_plan" :style="textColorPlan">
					<option v-for="(p, index) in plans" :value="index">{{p.name}}</option>
				</select>
			</div>
			</div>
			
		</div>
		<div class="col-xs-6 col-md-4">
			<h2 class="cart-tray text-right" :style="textColorPlan">View Cart</h2>
		</div>
	</div>
	<h1 class="text-center">Cart</h1>
	<table class="table">
		<thead>
			<th>Brand</th>
			<th>Model</th>
			<th>Price</th>
			<th>Quantity</th>
			<th>Options</th>
		</thead>
		<tbody>
			<tr v-for="(item, index) in cart">
				<td>{{item.brand}}</td>
				<td>{{item.model}}</td>
				<td>${{ getProductPrice(index)}}</td>
				<td>
					<input type="number" value="1" name="quantity">
				</td>
				<td>
					Edit |
					<button class="btn btn-sm btn-danger" type="button" @click="removeItem(item.id, index)">Remove</button>
				</td>
			</tr>
		</tbody>
	</table>
</div>

</template>

<script>

import { mapGetters, mapActions } from 'vuex'

export default {
	data () {
		return {
			current_plan: 0
		}
	},
	methods: {
		...mapActions([
			'removeCartItem'
		]),
		removeItem(id, index) {
			this.removeCartItem({
				id: id,
				index: index
			})
		},
		getProductPrice(cart_index) {
			switch(this.current_plan) {
				case 0:
					// Silver
					return this.cart[cart_index].price_silver * this.plans[this.current_plan].cost
				case 1:
					// Gold
					return this.cart[cart_index].price_gold * this.plans[this.current_plan].cost
				case 2:
					// Black
					return this.cart[cart_index].price_black * this.plans[this.current_plan].cost
			}
		}
	},
	computed: {
		...mapGetters({
			cart: 'getCart',
			plans: 'getPlans',
		}),
		getTotal() {
			let total = 0;
			for (let i=0; i<this.cart.length; i++) {
				total += this.getProductPrice(i)
			}
			return total.toFixed(2)
		},
		textColorPlan() {
			return {'color': this.current_plan == 2 ? 'white' : 'black' }
		}
	}
}

</script>

<style lang="scss" scoped>

.cart-tray {
	color: #000000;
}

h1, table, thead, tbody, span {
	color: #000000;
}



</style>