<template>
    <div>
        <h1>Board</h1>
        <svg id="board" :height="boardSize" :width="boardSize">
            <board-cell v-for="(cell, index) of board"
                v-bind:cell="cell"
                v-bind:size="cellSize"
                v-bind:key="index"
                @move="makeMove"
                >
            </board-cell>
        </svg>
        <h3>
            <small>Current player</small>
            <span>{{ player }}</span>
        </h3>
        <button @click="switchPlayers">Switch players</button>
        <button type="button" @click="clearBoard">Clear board</button>
        <div>
            <label>Board size:</label>
            <input v-model="boardSize">
        </div>
    </div>
</template>

<script>
    import Cell from './Cell.vue'

    export default {
        data() {
            return {
                board: [],
                players: ['X', 'O'],
                boardSize: 500
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
            }
        },
        methods: {
            makeMove(cell) {
                let index = cell.row * 3 + cell.col
                if (this.board[index].piece !== ' ') {
                    console.warn(`The square ${cell.row}, ${cell.col} `
                                 `already has ${cell.piece} in it!`)
                }
                this.board[index].piece = this.player
                this.switchPlayers()
            },
            switchPlayers() {
                let players = [this.opponent, this.player]
                this.players = players
            },
            clearBoard() {
                this.board = []
                // Build the board
                let id = 0
                for (var row = 0; row < 3; row++) {
                    for (var col = 0; col < 3; col++) {
                        this.board.push({id: id++, row, col, piece: ' '})
                    }
                }
            }
        },
        mounted() {
            this.clearBoard()
        },
        components: {
            'board-cell': Cell,
        }
    }
</script>
