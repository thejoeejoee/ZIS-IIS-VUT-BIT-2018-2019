import Vue from "vue";
import create from './store'
import Vuex from 'vuex'

const App = () => import('./App');

export default function install(el, initial = {}) {
    Vue.use(Vuex);
    return new Vue({
        el: el,
        render: h => h(App),
        store: create(initial),
    });
}