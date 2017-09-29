<template>
	<div class="container-fluid">
		<div class="col-xs-3"></div>
		<div style="margin:0px 0px 20px 0px; padding: 0px; background: rgba(255,255,255,0.23);" class="col-xs-6">
			<div style="padding:20px 10px 10px 15px">
				<p style="color: green; font-size: 25px; font-weight: bold;">Thank you, we have recieved your order.&nbsp;&nbsp;<i aria-hidden="true" class="fa fa-check"></i></p>
				<p>{{ successMessage1 }}</p>
				<p>{{ successMessage2 }}</p>
			</div>
			<div style="width:100%; text-align:center; margin:0px 0px 20px 0px;">
				<div v-if="getInvoicePDF">
					<div id="pdf">
							<object width="100%" height="500" type="application/pdf" :data="getInvoicePDF" id="pdf_content">
							<p>Error, reciept cannot be displayed at this time.</p>
							</object>
					</div>
				</div>
				<div v-else>
					<div id="pdf">
							<object width="100%" height="500" type="application/pdf" :data="getEstimatePDF" id="pdf_content">
							<p>Error, reciept cannot be displayed at this time.</p>
							</object>
					</div>
				</div>
			</div>
			<div v-show="upsell != ''" style="margin:0px 0px 0px 0px; background: rgba(255,255,255,0.30);" class="col-xs-12">
				<p style="padding-top:10px;"><i style="color: blue" class="fa fa-info-circle" aria-hidden="false"> &nbsp;</i>{{ upsell }}</p>
			</div>
		</div>
		<div v-if="getInvoicePDF" class="col-xs-12" style="width: 100%; text-align: center;">
			<a style="font-weight:bold" :download="'Mibura_SmartSupport_Invoice-' + localDate(new Date()) + '.pdf'" class="btn btn-lg btn-success" id="pdf-link" target="_blank" :href="getInvoicePDF">Download Receipt</a>
		</div>
		<div v-else class="col-xs-12" style="width: 100%; text-align: center;">
			<a style="font-weight:bold" :download="'Mibura_SmartSupport_Invoice-' + localDate(new Date()) + '.pdf'" class="btn btn-lg btn-success" id="pdf-link" target="_blank" :href="getEstimatePDF">Download Receipt</a>
		</div>
	</div>
</template>

<script>

import { mapGetters, mapActions } from 'vuex'
import {toJSONLocal} from '../scripts/functions'

export default {
	data(){
		return{
			upsell: 'Need to make any changes to your support plan? Please call 800.862.5144 or email support@mibura.com and we will get in touch with you in less than 15 minutes!',
			successMessage1: "An email confirmation has been sent to you.",
			successMessage2: "Please call us at 1.800.862.5144 if you have any questions about your order.",
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
			'getInvoicePDF',
			'getEstimatePDF',

		])
	},
	mounted() {
		if (!this.getInvoicePDF) {
			// this.serverGetInvoicePdf()
			console.log("No pdf file")
			if (!this.getEstimatePDF) {
				this.serverGetEstimatePdf()
			}
		}
	},
	methods: {
		...mapActions([
			'serverGetInvoicePdf',
			'serverGetEstimatePdf'
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
		},localDate(date) {
			return toJSONLocal(date)
		}
	}
}

</script>

<style scoped>

div h1 {
	color: white;
}

</style>