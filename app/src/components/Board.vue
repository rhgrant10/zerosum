<template>
    <div>
        <p>
            <button type="button" :disabled="isFresh" @click="reset" class="btn btn-sm btn-danger pull-right">
                <small>Reset</small>
            </button>
        </p>
        <svg id="board"
            :height="boardSize" :width="boardSize">
            <board-cell v-for="(cell, index) of board" :key="index"
                :cell="cell"
                :size="cellSize"
                :player="player"
                :is-game-over="isGameOver"
                @move="makeMove">
            </board-cell>
        </svg>
        <p>
            <label>Status:</label>
            <span>{{ status }}</span>
        </p>
    </div>
</template>

<script>
    import Cell from './Cell.vue'

    export default {
        data() {
            return {
                board: [],
                players: ['X', 'O'],
                boardSize: 590
            }
        },
        computed: {
            player() {
                return this.players[0]
            },
            opponent() {
                return this.players[1]
            },
            cellSize() {
                return this.boardSize / 3
            },
            winner() {
                if (this.board.length < 9) {
                    return
                }

                let lines = []
                for (var index = 0; index < 3; index++) {
                    var row = this.board.filter(cell => cell.row == index)
                    var col = this.board.filter(cell => cell.col == index)
                    lines = lines.concat([row, col])
                }
                // diagonals
                lines.push([this.board[0], this.board[4], this.board[8]])
                lines.push([this.board[2], this.board[4], this.board[6]])

                // check 'em
                for (var line of lines) {
                    if (this.isWinning(line)) {
                        line.forEach(cell => cell.isWinning = true)
                        return line[0].piece
                    }
                }
            },
            isFull() {
                return this.board.every(cell => !cell.isBlank)
            },
            isFresh() {
                return this.board.every(cell => cell.isBlank)
            },
            isDraw() {
                return !this.winner && this.isFull
            },
            status() {
                if (this.winner) {
                    return `${this.winner} wins!`
                } else if (this.isDraw) {
                    return 'Draw!'
                } else {
                    return `${this.player}, it's your turn.`
                }
            },
            isGameOver() {
                return this.isFull || this.winner
            }
        },
        methods: {
            isWinning(cells) {
                let first = cells[0]
                return !first.isBlank && cells.every(cell => cell.piece === first.piece)
            },
            makeMove(cell) {
                let index = cell.row * 3 + cell.col
                if (!this.board[index].isBlank) {
                    console.log(`The square ${cell.row}, ${cell.col} `
                                `already has ${cell.piece} in it!`)
                }
                this.board[index].piece = this.player
                this.board[index].isBlank = false
                this.switchPlayers()
            },
            switchPlayers() {
                let players = [this.opponent, this.player]
                this.players = players
            },
            reset() {
                this.players = ['X', 'O']
                this.board = []
                let id = 0
                for (var row = 0; row < 3; row++) {
                    for (var col = 0; col < 3; col++) {
                        this.board.push({
                            id: id++,
                            row,
                            col,
                            piece: '',
                            isBlank: true,
                            isWinning: false
                        })
                    }
                }
            }
        },
        mounted() {
            this.reset()
        },
        components: {
            'board-cell': Cell,
        }
    }
</script>

<style>
    p > h3 {
        display: inline;
    }
</style>