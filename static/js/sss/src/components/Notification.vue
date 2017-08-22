<template>
	<div :class="['alert alert-dismissable', 'alert-'+data.type]" role="alert">
		<button type="button" class="close" @click="remove_notification(index)" aria-label="Close"><span aria-hidden="true">&times;</span></button>
		{{ data.message }}
	</div>
</template>

<script>

import {mapActions} from 'vuex'

export default {
	props: [
		'data',
		'index'
	],
	methods: {
		...mapActions({
			remove_notification: 'removeNotification'
		})
	}
}

</script>

<style>

</style>