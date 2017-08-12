<template>
	<g :id="`cell-${cell.id}`" :transform="`translate(${x}, ${y})`"
		@click="handleClick">
		<rect ciass="cell" x="0" y="0" :width="size" :height="size"></rect>
		<text :font-size="size" :class="cell.piece">{{ cell.piece }}</text>
	</g>
</template>

<script>
	export default {
		data() {
			return {}
		},
		props: ['cell', 'size'],
		computed: {
			x() { return this.size * this.cell.col },
			y() { return this.size * this.cell.row }
		},
		methods: {
			handleClick() {
				if (!this.cell.piece.trim()) {
					this.$emit('move', this.cell)
				}
			}
		}
	}
</script>

<style>
	g > rect {
		fill: burlywood;
		boarder: .02em solid brown;
	}
	g > text {
		dominant-baseline: text-before-edge;
		padding-left: .5em
	}
	.X {
		fill: maroon;
	}
	.O {
		fill: skyblue;
	}
</style>
