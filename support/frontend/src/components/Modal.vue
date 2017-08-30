<template>
	<div class="modal fade" id="chatModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
					<h4 class="modal-title" id="myModalLabel">Contact Sales</h4>
				</div>
				<div class="modal-body text-center">
					<h3>Cart Reference Code<br>{{get_cart_reference}}</h3>
				</div>
				<div class="modal-footer">
					<a href="tel:1-800-862-5144" class="btn btn-primary">Call Now <i class="fa fa-phone" aria-hidden="true"></i></a>
					<button type="button" class="btn btn-info openchat">Chat Now <i class="fa fa-comment" aria-hidden="true"></i></button>
					<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

export default {
	props: [
		'id',
		'title',
		'body',
		'buttons'
	]
}

</script>