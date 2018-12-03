import Vue from "vue";
import create from './store'
import Vuex from 'vuex'
import Axios from "axios";
import toastr from "toastr";

const App = () => import('./App');

export default function install(el, initial = {}) {
    Vue.use(Vuex);
    const moment = require('moment');
    require('moment/locale/cs');

    Vue.use(require('vue-moment'), {moment});
    Axios.interceptors.response.use(null, function (error) {
        error.response.status === 403 && toastr.warning(initial.trans.no_perms);
        return Promise.reject(error);
    });


    return new Vue({
        el: el,
        render: h => h(App),
        store: create(initial),
    });
}