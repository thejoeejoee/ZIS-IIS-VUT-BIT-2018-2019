import Vue from 'vue'
import './scss/styles.js'
import 'bootstrap/js/dist/collapse'
import 'toastr/build/toastr.min.css'
import 'jquery'
import toastr from 'toastr'
import installEnclosureList from './components/EnclosureList/main';
import installRangePlanning from './components/RangePlanning/main';
import installCalendar from './components/Calendar/main';
import replaceSvgImg from './utils/svg';

import 'bootstrap-duration-picker/dist/bootstrap-duration-picker'
import Axios from "axios";


Vue.config.productionTip = false;

Axios.interceptors.response.use(null, function (error) {
    error.response.status === 403 && toastr.warning('Sorry, no permissions for this action.');
    return Promise.reject(error);
});


window.$ = window.jQuery = require("jquery");
window.toastr = require("toastr");
window.zis = {
    installEnclosureList,
    installRangePlanning,
    installCalendar,
    replaceSvgImg,
};