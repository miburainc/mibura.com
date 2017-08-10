import {URL_ROOT, API_ROOT} from '../values'
import axios from 'axios'

const actions = {
	getProductCategories(success) {
		console.log("products.js/getProductCategories")
		axios.get(API_ROOT + 'categories/')
		.then((response) => {
			success(response)
		})
		.catch((error) => {
			console.error(error)
		})
	}
}

export default {
	...actions
}
