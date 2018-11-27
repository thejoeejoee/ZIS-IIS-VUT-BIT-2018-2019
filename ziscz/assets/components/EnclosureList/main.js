import Vue from "vue";
import create from './store'
import Vuex from 'vuex'
import VuexUndoRedo from 'vuex-undo-redo';

const App = () => import('./App');

export default function install(el, initial = {}) {
    Vue.use(Vuex);
    Vue.use(VuexUndoRedo);

    const moment = require('moment');
    require('moment/locale/cs');

    Vue.use(require('vue-moment'), {moment});
    return new Vue({
        el: el,
        render: h => h(App),
        store: create(initial),
    });
}