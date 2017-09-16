<template>
	<div class="container-fluid">
		<div class="col-xs-3"></div>
		<div style="margin:0px 0px 20px 0px; padding: 0px; background: rgba(255,255,255,0.23);" class="col-xs-6">
			<div style="padding:10px">
				<p style="color:white;">{{ successMessage }}</p>
			</div>

			<div style="margin:0px 0px 0px 0px; padding:10px 0px 10px 10px; border-top: 1px solid lightgray" class="col-xs-12">
				<h3>{{ getPlan(getCurrentPlan).name }}</h3><h4>{{ writeOutSupportLength() }}</h4>
				
			</div>
			
			<br>
			<!-- <h4>Cart Reference Code: {{ getCartReference }}</h4> -->
			<div style="margin:0px 0px 0px 0px; padding: 0px 0px 0px 0px;" class="col-xs-12">
				<table class="table table-hover table-outline" style="margin-bottom: 15px; border-bottom: 1px solid lightgray;">
<!-- 					<thead>
						<th style="padding-left:10px">Product</th>
						<th style="padding-left:10px">Price</th>
					</thead> -->
					<tbody>
						<tr v-for="(item, index) in getCart">
							<td style="color:white; padding-left:15px;" >{{ item.brand }} {{ item.model }}</td>
							<td style="color:white; text-align:right; padding-right:15px;" >${{ numWithCommas(getProductSubtotal(index)-getProductSubtotal(index)*getCurrentDiscount) }}</td>
						</tr>
					</tbody>
				</table>
			</div>
			<!-- <p class="pad-5">Cart Reference ID: {{ getCartReference }}</p>
			<div class="pad-5">
				<h4>Your information:</h4>
				<div v-if="Object.keys(getClientInfo).length > 0">
					<div v-for="key in Object.keys(getClientInfo)">
						{{key}}: {{getClientInfo[key]}}
					</div>
					<br>
					<button type="button" class="btn btn-link" @click="buttonEditClient">Edit</button>
				</div>
				<div v-else>
					<button type="button" class="btn btn-default" @click="buttonStartClientInfo">Enter your information</button>
				</div>
			</div> -->
			<div class="col-md-9"></div>
			<div class="col-xs-12 col-md-3" style="padding: 15px 15px 15px 7px; text-align:right;">
				<p style="margin:0px">SubTotal:  ${{ numWithCommas(getTotal) }}</p>
				<p style="margin:0px">%{{getCurrentDiscount*100}} Discount:
				 ${{numWithCommas(getTotal*getCurrentDiscount)}}</p>
				<span style="font-size: 1.5em;font-weight:700;">Payment Total: ${{ numWithCommas(getGrandTotal) }}</span>
			</div>
			<div v-show="upsell != ''" style="margin:0px 0px 0px 0px; padding-top:0px; background: rgba(255,255,255,0.30);" class="col-xs-12">
				<!-- <button class="btn btn-lg btn-outline-info"><i style="color: #3285C4" class="fa fa-info-circle" aria-hidden="false"> &nbsp</i>{{ upsell }}</button> -->
			</div>
		</div>
	</div>
</template>

<script>

import { mapGetters, mapActions } from 'vuex'

export default {
	data(){
		return{
			upsell: '',
			successMessage: 'Congratulations, you just checked out with Mibura Smart Support! An email confirmation has been sent to you.'
		}
	},
	computed: {
		...mapGetters([
			'numWithCommas',
			'getPlan',
			'getCurrentPlan',
			'getCart',
			'getCartReference',
			'getSupportMonths',
			'getProductSubtotal',
			'getTotal',
			'getGrandTotal',
			'getCurrentDiscount',
		])
	},
	methods: {
		...mapActions([
			
		]),
		writeOutSupportLength() {
			let str = ""
			let lenArray = String(this.getSupportMonths/12).split('.')
			if (lenArray.length > 1) {
				if(lenArray[0] == 1){
					str = lenArray[0] + " Year & 6 months"	
				}
				else if(lenArray[0] != 0){
					str = lenArray[0] + " Years & 6 months"		
				}
				else{
					str = "6 months"
				}
			}
			else {
				if(lenArray[0] == 1){
					str = lenArray[0] + " Year"	
				}
				else if(lenArray[0] != 0){
					str = lenArray[0] + " Years"
				}
			}
			return str
		}
	}
}

</script>

<style scoped>

div h1 {
	color: white;
}

</style>