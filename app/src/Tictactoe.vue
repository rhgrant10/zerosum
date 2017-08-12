<template>
    <div>
        <div class="row">
            <div class="col-xs-7">
                <board></board>
            </div>
            <div class="col-xs-5">
                <history></history>
            </div>
        </div>
    </div>
</template>

<script>
    import Board from './components/Board.vue'
    import History from './components/History.vue'

    export default {
        data () {
            return {}
        },
        components: {
            'board': Board,
            'history': History
        }
    }
</script>
