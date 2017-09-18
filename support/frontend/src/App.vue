<template>
	<div id="app" class="container-fluid">
		<!-- Confirm Terms and conditions -->
		<div class="modal fade" id="termsModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Terms and conditions</h4>
					</div>
					<div class="modal-body">
						Terms and conditions body.
						<p>
							Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut elit arcu, lacinia vel erat vel, feugiat finibus eros. Vivamus porttitor libero vel dui vestibulum pharetra. Cras ornare massa non purus porttitor, quis vestibulum lorem feugiat. Donec eget posuere eros. Vivamus eget tellus vitae enim placerat elementum. Nulla a justo et risus molestie vehicula. Morbi nec libero ut neque facilisis scelerisque ac quis tellus. Etiam efficitur efficitur ultricies. Sed hendrerit porttitor erat vel dictum. Nam ultrices magna ultrices maximus ultrices. Nunc venenatis vehicula odio, vitae vestibulum enim. Suspendisse tempus lorem lacus, ac rhoncus dui dictum non. Integer sed sagittis urna. Nulla lacinia cursus velit vel egestas. Pellentesque sollicitudin bibendum erat, ac tristique odio lacinia id.
						</p><p>
							Ut vehicula lobortis velit, vel iaculis mauris imperdiet non. Aliquam sed velit vitae nulla pellentesque consequat. Aliquam ac consectetur mi, non tristique diam. Suspendisse potenti. Nunc lectus libero, facilisis eu odio quis, euismod mollis mi. Suspendisse tincidunt sit amet purus eu laoreet. Fusce egestas, metus et viverra ultrices, ante dolor egestas est, at pharetra purus velit quis dui. Fusce pretium purus vel magna ullamcorper molestie. Donec venenatis tempor sem sed feugiat. Nunc eu sollicitudin felis. Etiam tempus mollis condimentum. Morbi turpis metus, tristique eu augue porttitor, venenatis sagittis justo.
						</p><p>
							Maecenas et magna sed tortor interdum facilisis id vitae diam. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut id odio ultrices erat congue blandit non imperdiet augue. Fusce porta rhoncus enim, sit amet faucibus ante sagittis sit amet. Vestibulum commodo, sem ac sollicitudin auctor, felis ante commodo erat, eget iaculis ipsum eros a odio. Etiam suscipit, purus at tempus bibendum, velit dui varius ligula, ut blandit nisl dui non quam. Vestibulum magna dolor, tristique vel enim eget, cursus vulputate massa. Nulla non mattis diam, ut blandit orci. Nullam aliquam cursus pellentesque. Sed euismod fermentum ligula.
						</p><p>
							Proin at congue nisi. Etiam dui massa, scelerisque quis malesuada non, pulvinar convallis libero. Maecenas dictum eu velit quis faucibus. Etiam eget lectus id arcu rhoncus tempus. Nam non erat diam. Nunc ligula magna, pellentesque vitae sem ac, luctus mollis nisi. Suspendisse cursus iaculis neque, nec commodo lectus posuere quis. Ut quis laoreet ex. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum vitae nisi vel nunc dictum dignissim et ut risus. Ut odio ipsum, pulvinar vitae suscipit eu, aliquet quis lorem. Nam sit amet gravida urna. Donec porta blandit justo, quis luctus erat semper in. Phasellus eget scelerisque metus.
						</p><p>
							Morbi ac nunc viverra, dictum leo non, pulvinar nunc. Nunc bibendum, odio nec fermentum fermentum, lacus nisl volutpat nisi, sed consectetur nulla risus consectetur velit. Aenean luctus accumsan posuere. Donec in eros sollicitudin, vehicula felis eu, consectetur ipsum. Nam aliquet posuere erat id accumsan. Praesent porta mollis faucibus. Praesent ac lobortis risus, vitae pharetra risus.
						</p><p>
							Aenean et elit vel risus finibus rutrum faucibus vel est. Pellentesque auctor elit at accumsan finibus. Nullam quam leo, imperdiet vestibulum volutpat id, facilisis nec mauris. Donec velit augue, tempus et ante non, suscipit malesuada eros. Integer eu ex in enim interdum vehicula. Aliquam ut congue arcu. Quisque molestie mauris in ipsum laoreet, aliquet laoreet orci congue. Donec molestie imperdiet neque nec sollicitudin. Ut a lacus pretium metus volutpat tempus. Quisque pulvinar diam eget nulla consequat, sit amet tincidunt eros aliquet. Duis dapibus massa nisi, non venenatis ipsum tempus maximus. Nulla luctus feugiat tempus. Curabitur sed facilisis justo. Sed dictum ex sed blandit tempus. Duis non ante porttitor, mollis felis tempus, ultricies quam. Nunc mattis dictum lacinia.
						</p><p>
							Donec ac ex nec orci suscipit iaculis ut vitae magna. Aenean non elit metus. In rhoncus elementum orci, in tincidunt leo porttitor vel. Phasellus at pretium turpis, sit amet interdum ex. Duis vitae erat in dolor porttitor varius ut et sapien. Vivamus turpis augue, tempus ac turpis a, rutrum rhoncus magna. Donec scelerisque faucibus bibendum. Vestibulum auctor, leo nec viverra rutrum, neque turpis ultricies turpis, at mattis arcu lorem in leo. Quisque ante enim, elementum nec luctus id, posuere vitae sapien.
						</p><p>
							Quisque luctus lectus a consequat pharetra. Donec quis lorem in sem porta ultricies non at ex. Mauris sodales leo vitae ante elementum, condimentum molestie purus rutrum. Nunc vulputate posuere enim, ut blandit purus rutrum eu. Vivamus accumsan vulputate risus. In sit amet purus ante. Phasellus et vulputate purus, eu finibus est. Nulla eleifend varius leo ac ullamcorper. Sed eget elit in magna scelerisque rutrum. Aenean porttitor augue in enim efficitur, hendrerit commodo leo tincidunt. Phasellus elementum sodales tempus.
						</p>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
						<button type="button" class="btn btn-primary" @click="setAcceptedTerms(true)" data-dismiss="modal">Accept</button>
					</div>
				</div>
			</div>
		</div>
		<!-- Info for ach payment -->
		<div class="modal fade" id="achInfoModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Payment by ACH</h4>
					</div>
					<div class="modal-body">
						<p>
							In order to pay with a bank account number we must first confirm your account.  To do this we will deposit two small ammounts into your bank account.  Once you recieve the payments you can come back to this site and tell us the ammounts to confirm that you are the owner of the account.  To speed up the process you can get an estimate and use your cart reference code to quickly return to where you left off.  If you have any questions, please contact us at 1-800-862-5144.
						</p>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
					</div>
				</div>
			</div>
		</div>
		<!-- Popup when user submits ach using account number and routing number -->
		<div class="modal fade" id="achSubmitModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Payment by ACH</h4>
					</div>
					<div class="modal-body">
						<p>
							In order for us to process your payment we will need to confirm that your account is valid. To do this we will deposit two small ammounts into your bank account.  Once you recieve the payments you can come back to this site and enter the ammounts to finish the confirmation.  To speed up the process you can get an estimate and use your cart reference code to quickly return to where you left off.  After this you will be able to review your order and choose to initiate payment.  
							<br><br>
							We will send you an email with a quote of your order and a link to return to confirm your payment ammounts.
							<br><br>
							If you have any questions, please contact us at 1-800-862-5144.
						</p>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Back</button>
						<button type="button" class="btn btn-primary" @click="confirmAch" data-dismiss="modal">Continue</button>
					</div>
				</div>
			</div>
		</div>
		<!-- Input Estimate ID -->
		<div class="modal fade" id="estimateIdModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h4 class="modal-title" id="myModalLabel">Open Estimate</h4>
					</div>
					<div class="modal-body" style="overflow-y: scroll;">
						<h4>Input Estimate ID</h4>
						<input style="color: #000000;" type="text" name="estimate_id" class="form-control" v-model="estimate_id" autofocus>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
						<button type="button" class="btn btn-primary" @click="requestPastQuote">Request</button>
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
					<div class="modal-body" style="overflow-y: scroll;">
						
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
						<button type="button" class="btn btn-primary">Submit Payment</button>
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
						<h4 class="modal-title" id="myModalLabel">Download or Print Estimate</h4>
					</div>
					<div class="modal-body">
						<div v-if="getEstimatePDF">
							<h4>Your estimate is ready!</h4>
							<div id="pdf">
  								<object width="100%" height="500" type="application/pdf" :data="getEstimatePDF" id="pdf_content">
    								<p>Insert your error message here, if the PDF cannot be displayed.</p>
  								</object>
							</div>
						</div>
						<div v-else>
							<h4>Processing</h4>
							<button class="btn btn-lg btn-success" type="button" disabled="true">
								<i class="fa fa-circle-o-notch fa-spin" style="font-size:24px"></i>
							</button>
						</div>
					</div>
					<div class="modal-footer">
						<a v-if="getEstimatePDF" :download="'Mibura_SmartSupport_Estimate-' + localDate(new Date()) + '.pdf'" class="btn btn-success" id="pdf-link" target="_blank" :href="getEstimatePDF">Download PDF</a>
						<button v-if="getEstimatePDF" type="button" class="btn btn-primary" @click="emailQuote">Receive in Email</button>
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
						<h3>Cart Reference Code<br>{{getCartReference}}</h3>
					</div>
					<div class="modal-footer">
						<a href="tel:1-800-862-5144" class="btn btn-primary">Call Now <i class="fa fa-phone" aria-hidden="true"></i></a>
						<button type="button" class="btn btn-info openchat">Chat Now <i class="fa fa-comment" aria-hidden="true"></i></button>
						<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
					</div>
				</div>
			</div>
		</div>
		<div v-if="getPurchaseSuccess" class="row">
			<success-screen></success-screen>
		</div>
		<div v-else class="row">
			<div class="col-xs-12">
				<progressbar></progressbar>
			</div>
			<div class="col-md-12 col-lg-3" style="padding: 0 5px;">
				<notification v-for="(notification, index) in getNotifications" :data="notification" :index="index" :key="index"></notification>
			</div>
			<div id="support-form" class="col-xs-10 col-xs-offset-1 col-md-8 col-md-offset-0 col-lg-6 col-lg-offset-0">
				<support-form class="pad-10"></support-form>
			</div>
			<div id="side_cart_container" class="side-cart col-xs-12 col-md-4 col-lg-3" >
				<side-cart></side-cart>
			</div>
			<!-- <div id="cart" class="mobile-cart col-xs-12">
				<support-cart></support-cart>
			</div> -->
		</div>
	</div>
</template>

<script>

import SupportForm from './components/Form.vue'
import SupportCart from './components/Cart.vue'
import SideCart from './components/Cart_Side.vue'
import SuccessScreen from './components/SuccessScreen.vue'
import Notification from './components/Notification.vue'
import Progressbar from './components/ProgressBar.vue'

import {toJSONLocal} from './scripts/functions'

import {mapActions,mapGetters} from 'vuex'

import axios from './store/api/api-config'

export default {
	name: 'app',
	data () {
		return {
			estimate_id: '',
			stripe: null
		}
	},
	components: {
		SupportForm,
		SupportCart,
		SuccessScreen,
		SideCart,
		Notification,
		Progressbar
	},
	computed: {
		...mapGetters([
			'getCartReference',
			'getPurchaseSuccess',
			'getEstimatePDF',
			'getNotifications',
			'getAPIRoot',
			'getClientInfo',
			'getPaymentInfo',
			'getCart',
			'getCartChanged',
			
		])
	},
	methods: {
		...mapActions([
			'setCategoryMultipliers',
			'setDiscounts',
			'setAcceptedTerms',
			'ServerRequestPastEstimate',
			'sendQuoteEmail',
			'setCloudProviders',
			'setCurrentFormStep',
			'setEstimatePdfFile',
			'achSendCredentials',
			'serverGetEstimatePdf',
			'serverSetClient',
			'saveCart',
			'setPaymentProp',
		]),
		emailQuote() {
			this.sendQuoteEmail()
		},
		requestPastQuote() {
			this.ServerRequestPastEstimate(this.estimate_id)
		},
		localDate(date) {
			return toJSONLocal(date)
		},
		confirmAch(){

			//finish submission of ach
			let payload = {
				'cart_ref': null,
				'accountnumber': this.getPaymentInfo['accountnumber'],
				'bankname': this.getPaymentInfo['bankcustomername'],
				'bankphone': this.getPaymentInfo['bankphone'],
				'routingnumber': this.getPaymentInfo['routingnumber']
			}

			this.stripe.createToken('bank_account', {
				country: 'us',
				currency: 'usd',
				routing_number: this.getPaymentInfo['routingnumber'],
				account_number: this.getPaymentInfo['accountnumber'],
				account_holder_name: this.getPaymentInfo['bankcustomername'],
				account_holder_type: this.getPaymentInfo['accounttype'],
			}).then((results) => {
				// handle result.error or result.token
				console.log(results.token)
				this.setPaymentProp({ prop: 'banktoken', data: results.token.id})
				this.setPaymentProp({ prop: 'bankname', data: results.token.bank_account.bank_name})

				// Reset pdf to nothing
				this.setEstimatePdfFile(null);
				// Send request for new pdf file
				this.serverSetClient().then(() => {
					this.saveCart(this.getClientInfo)
				// }).then(() => {
					// this.serverGetEstimatePdf()
				}).then(() => {
					payload['cart_ref'] = this.getCartReference
					console.log("SEND PAYLOAD TO API ENDPOINT")
					console.log(payload)
					this.achSendCredentials(this.getPaymentInfo['banktoken'])
				})
				
			});


			
			
			
			//GO TO SUCCESS PAGE
		}
	},
	mounted() {
		setTimeout(() => {
			this.stripe = Stripe('pk_test_jW4CJTGamhoH2cCxQljIKiwd');
		}, 1000)
		
		axios.get(this.getAPIRoot + 'cloud')
			.then((response) => {
				console.log(response)
				this.setCloudProviders(response.data.results)
			})
			.catch((error) => {
				console.error(error)
			})
		this.setCategoryMultipliers()
		this.setDiscounts()
	}
}
</script>

<style lang="scss">

#app {
	padding-top: 40px;
}

h1, h2, h3, h4 {
	margin: 0;
}

.btn-2, .btn-3, .btn-4 .btn-3-round .btn-2-round {
	width: 100%;
}

.btn-4 .btn {
	width: 24.95%;
} 

.btn-3 button.btn {
	margin: 0;
	margin-left: 0!important;
	border-radius: 0;
	width: 33.33%;
} 

.btn-3-round button.btn {
	margin: 0;
	margin-left: 0!important;
	width: 33.33%;
}

.btn-2 .btn {
	margin: 0;
	margin-left: 0!important;
	border-radius: 0;
	width: 50%!important;
}

.btn-2-round .btn {
	margin: 0;
	margin-left: 0!important;
	width: 50%!important;
}

.btn-plan {
	width: 33.33%;
	padding: 10px;
	border: 0;
}

.mobile-cart {
	display: none;
}

#side_cart {
	-webkit-box-shadow: 2px 10px 20px 1px rgba(0,0,0,0.7);
	-moz-box-shadow: 2px 10px 20px 1px rgba(0,0,0,0.7);
	box-shadow: 2px 10px 20px 1px rgba(0,0,0,0.7);
}

.modal .modal-body {
    max-height: 420px;
    overflow-y: auto;
}

#support-form {
	display: block;
	z-index: 0;
	min-height: 100%;
	min-height: 100vh;
}


</style>
