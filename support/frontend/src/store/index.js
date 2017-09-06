import Vue from 'vue';
import Vuex from 'vuex'

import Form from './modules/sss_form'
import Cart from './modules/sss_cart'

import {API_ROOT, product_multiplier} from './values'

import createLogger from '../scripts/logger'

import getters from './getters'
import actions from './actions'
import mutations from './mutations'

import moment from 'moment'

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production'

export const store = new Vuex.Store({
  state: {
    api_root: API_ROOT,
    errors: {},
    multiplier: {},
    brands: [],
    purchase_success: false,
    accepted_terms: false,
    stripe: {},
    discounts: [],
    current_discount: 0.0,
  },
  getters,
  mutations,
  actions,
  modules: {
  	Form,
    Cart,
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
})