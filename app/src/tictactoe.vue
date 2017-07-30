<template>
	<div class="row">
		<div class="col-xs-7">
			<board></board>
		</div>
		<div class="col-xs-5">
			<history></history>
		</div>
	</div>
</template>

<script>
	import Board from './components/board.vue'
	import History from './components/history.vue'

	export default {
		data () {
			return {

			}
		},
		components: {
			Board,
			History
		}
	}
</script>
