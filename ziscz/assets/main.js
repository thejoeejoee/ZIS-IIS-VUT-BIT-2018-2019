import Vue from 'vue'
import './scss/styles.js'
import 'bootstrap/js/dist/collapse'
import 'toastr/build/toastr.min.css'
import installEnclosureList from './components/EnclosureList/main';
import installCleaningPlanning from './components/CleaningPlanning/main';

window.$ = window.jQuery = require("jquery");
window.toastr = require("toastr");

Vue.config.productionTip = false;


window.zis = {
    installEnclosureList,
    installCleaningPlanning
};