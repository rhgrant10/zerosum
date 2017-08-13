import Vue from 'vue'
import VueResource from 'vue-resource';

import Ttt from './Tictactoe.vue'


Vue.use(VueResource);

new Vue({
    el: '#app',
    render: h => h(Ttt)
})
