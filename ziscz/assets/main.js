import Vue from 'vue'
import './scss/styles.js'
import 'bootstrap/js/dist/collapse'
import 'toastr/build/toastr.min.css'
import 'jquery'
import installEnclosureList from './components/EnclosureList/main';
import installRangePlanning from './components/RangePlanning/main';
import installCalendar from './components/Calendar/main';
import replaceSvgImg from './utils/svg';

import 'bootstrap-duration-picker/dist/bootstrap-duration-picker'


Vue.config.productionTip = false;


window.$ = window.jQuery = require("jquery");
window.toastr = require("toastr");
window.zis = {
    installEnclosureList,
    installRangePlanning,
    installCalendar,
    replaceSvgImg,
};