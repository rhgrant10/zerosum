<template>
	<g :id="`cell-${cell.id}`" :transform="`translate(${x}, ${y})`"
		@click="move" @mouseover="showHint = true" @mouseleave="showHint = false">
		<rect ciass="cell" x="0" y="0" :width="size" :height="size" :style="cellStyle"></rect>
		<text :font-size="size" :class="display" :x="size / 2" :y="size / 2">
			{{ display }}
		</text>
	</g>
</template>

<script>
	export default {
		props: ['cell', 'size', 'player', 'isGameOver'],
		data() {
			return {
				showHint: false
			}
		},
		computed: {
			x() {
				return this.size * this.cell.col
			},
			y() {
				return this.size * this.cell.row
			},
			cellStyle() {
				let style =  {'stroke-width': this.size / 20}
				if (this.cell.isWinning) {
					style['fill'] = 'slategrey'
				}
				return style
			},
			display() {
				if (!this.isGameOver && this.cell.isBlank && this.showHint) {
					return this.player
				} else {
					return this.cell.piece
				}
			}
		},
		methods: {
			move() {
				if (!this.isGameOver && this.cell.isBlank) {
					this.$emit('move', this.cell)
				}
			}
		}
	}
</script>

<style>
	g > rect {
		fill: black;
		stroke: lightgrey;
	}
	g > text {
		dominant-baseline: central;
		text-anchor: middle;
	}
	.X {
		fill: crimson;
	}
	.O {
		fill: royalblue;
	}
</style>
