<template>
	<div class="barWrapper">
		<!-- <span class="progressText"><B>Progress</B></span> -->
		<div 
			id="progressBar" 
			class="progress tip"
			title="tippy" 
		>
			<div id="progressbarcolor" class="progress-bar progress-bar-striped" role="progressbar" :aria-valuenow="(get_current_step/get_formsteps.length)*100" aria-valuemin="0" aria-valuemax="100" :style="{'width': ((get_current_step+1)/get_formsteps.length)*100+'%'}">   
			</div>
		</div>
	</div>
</template>

<script>

import {mapGetters, mapActions} from 'vuex'

export default {
	data() {
		return {
			tip: null,
			last_tooltip_value: 0,
		}
	},
	mounted() {
		this.tip = tippy('.tip', {
			position: 'top',
			animation: 'scale',
			duration: 0,
			arrow: true,
			followCursor: true,
			dynamicTitle: true,
			stickyDuration: 10000,
			flipDuration: 0,
		});
		var intervalId;
		$('#progressBar').mousemove((e) => {
			var offsets = $('#progressBar').offset();
			var left = offsets.left;
			var x = e.pageX - left;

			let formsteps_length = this.get_formsteps.length
			var startPos = document.getElementById('progressBar').position;
			var barWidth = $('#progressBar').width()
			var xconvert = (x/barWidth)


			let num = formsteps_length * xconvert
			let roundnum = Math.floor(num)
			
			if (this.last_tooltip_value != roundnum) {
				let tip = this.tip
				const el = document.querySelector('.tip')
				const popper = tip.getPopperElement(el)
				
				var title = this.get_formsteps[roundnum].title
				$('.tip').attr('title', title).attr('data-old-title', title)
				tip.update(popper, 0)
				this.last_tooltip_value=roundnum
			}
		});

		document.getElementById('progressBar').addEventListener('click', (e) => {
			var offsets = $('#progressBar').offset();
			var left = offsets.left;
			var x = e.pageX - left;

			let formsteps_length = this.get_formsteps.length

			var startPos = document.getElementById('progressBar').position;
			var barWidth = $('#progressBar').width()
			var xconvert = x/barWidth;
			
			let roundnum = Math.floor(formsteps_length * xconvert)

			

			console.log(roundnum)

			this.set_current_form_step(roundnum)
		});
	},
	methods: {
		...mapActions({
			set_current_form_step: 'setCurrentFormStep',
		})
	},
	computed: {
		...mapGetters({
			get_formsteps: 'getFormSteps',
			get_current_step: 'getCurrentFormStep',
		})
	}
}

</script>

<style scoped>

.barWrapper {
	margin-top: 15px;
	margin-bottom: 15px;

	-webkit-box-shadow: 2px 5px 8px .5px rgba(0,0,0,0.1);
	-moz-box-shadow: 2px 5px 8px .5px rgba(0,0,0,0.1);
	box-shadow: 2px 5px 8px .5px rgba(0,0,0,0.1);
}

#progressBar {
    width:100%;
    height: 16px;
}

#progressBar:hover {
	cursor: pointer;
}



.progress {
	border-radius:0;
	overflow:visible;
	margin-bottom: 2px;
}

.progress-bar {
	// background:rgb(23,44,60); 
	-webkit-transition: width .5s ease-in-out;
	transition: width .5s ease-in-out;
}
</style>