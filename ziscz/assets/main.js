import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App'
import './scss/styles.js'
import store from './store'
import 'bootstrap/js/dist/collapse'

window.$ = window.jQuery = require("jquery");


const HomePage = () => import('./pages/HomePage');

Vue.use(VueRouter);

const router = new VueRouter({
    routes: [
        {path: '/', component: HomePage, name: 'home'},
    ],
    mode: 'history',
    linkActiveClass: 'active',
    linkExactActiveClass: 'active',
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        } else {
            return {x: 0, y: 0}
        }
    }
});

Vue.config.productionTip = false;
new Vue({
    el: '#app',
    render: h => h(App),
    router,
    store,
});