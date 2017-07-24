import * as TYPE from '../types'

const STEPS = [
	{
		data: [
			{
				placeholder: "Brand Name",
				src: "brand",
				dest: "cart.#.brand",
				required: true,
				form: {
					type: "text",
					name: "brand",
				},
				validate: {
					type: "text",
					min: 3,
				}
			},
		],
		buttons: [
			{
				label: "Next",
				class: "btn btn-success",
				script: "next"

			},
		],
		title: "Brand",
		text: "Please type your hardware's brand",
		error: "We aren't sure if we support this brand.  Please check the spelling, or contact us to find out if we can support it!",
		step: 0,
	},
	{
		data: [
			{
				placeholder: "Model Name",
				src: "model",
				dest: "cart.#.model",
				required: true,
				form: {
					type: "text",
					name: "model"
				},
				validate: {
					min: 3
				},
			},
		],
		buttons: [
			{
				label: "Back",
				class: "btn btn-default",
				script: "back"
			},
			{
				label: "Next",
				class: "btn btn-success",
				script: "next"

			},
		],
		title: "Model",
		text: "Please type the model name.",
		error: "We aren't sure if we support this model.  Please check the spelling, or contact us to find out if we can support it!",	
		step: 0,
	},
	{
		data: [
			{
				placeholder: "Serial Number",
				src: "",
				dest: "cart.#.sn",
				required: false,
				form: {
					type: "text",
					name: "serialnumber"
				},
				validate: {},
			},
			{
				placeholder: "Device Age (Years)",
				src: "",
				dest: "cart.#.age",
				required: false,
				form: {
					type: "number",
					name: "deviceage",
				},
				validate: {}
			},
			{
				placeholder: "Addditional Info",
				src: "",
				dest: "cart.#.info",
				required: false,
				validate: {},
				form: {
					name: "additionalinfo",
					type: "textarea"
				}
			},
		],
		buttons: [
			{
				label: "Back",
				class: "btn btn-default",
				script: "back"
			},
			{
				label: "Next",
				class: "btn btn-success",
				script: "next"

			},
		],
		title: "Additional Information",
		text: "These fields are all optional, but please supply us with as much information as you can to ensure we provide you with the best support!",
		error: "",
		step: 0,
	},
	{
		data: [
			{
				placeholder: "Cloud Provider",
				src: "cloud",
				dest: "cart.#.cloud",
				required: false,
				validate: {},
				form: {
					type: "select",
					name: "cloudprovider",
				}
			},
		],
		buttons: [
			{
				label: "Back",
				class: "btn btn-default",
				script: "back"
			},
			{
				label: "Add Another",
				class: "btn btn-default",
				script: "additem,start"
			},
			{
				label: "Next",
				class: "btn btn-success",
				script: "additem,next"

			},
		],
		title: "Cloud Provider",
		text: "Add a cloud provider",
		error: "",
		step: 0,
	},
	{
		data: [
			{
				placeholder: "First Name",
				dest: "client.first_name",
				required: true,
				validate: {
					type: "text", 
					min: 3
				},
				form: {
					type: "text",
					name: "firstname",
				}
			},
			{
				placeholder: "Last Name",
				src: "",
				dest: "client.last_name",
				required: true,
				validate: {
					type: "text", 
					min: 3
				},
				form: {
					type: "text",
					name: "lastname",
				}
			},
			{
				placeholder: "Company",
				src: "",
				dest: "client.company",
				required: true,
				validate: {
					type: "text", 
					min: 3
				},
				form: {
					type: "text",
					name: "company",
				}
			},
			{
				placeholder: "Phone Number",
				src: "",
				dest: "client.phone",
				required: true,
				validate: {
					type: "phone",
					min: 6,
				},
				form: {
					type: "text",
					name: "phonenumber",
				}
			},
			{
				placeholder: "Email Address",
				src: "",
				dest: "client.email",
				required: true,
				validate: {
					type: "email",
				},
				form: {
					type: "text",
					name: "email",
				}
			},
		],
		buttons: [
			{
				label: "Next",
				class: "btn btn-success",
				script: "next"

			},
		],
		title: "Personal Information",
		text: "",
		error: "",
		step: 1,
	},
	{
		data: [
			{
				placeholder: "Street",
				src: "",
				dest: "client.address.street",
				required: true,
				validate: {
					type: "text", 
					min: 3,
				},
				form: {
					type: "text",
					name: "street1",
				}
			},
			{
				placeholder: "Street 2",
				src: "",
				dest: "client.address.street_secondary",
				required: false,
				validate: {},
				form: {
					type: "text",
					name: "street2",
				}
			},
			{
				placeholder: "City",
				src: "",
				dest: "client.address.city",
				required: true,
				validate: {
					type: "text", 
					min: 3,
				},
				form: {
					type: "text",
					name: "city",
				}

			},
			{
				placeholder: "State",
				src: "",
				dest: "client.address.state",
				required: true,
				validate: {
					min: 2,
				},
				form: {
					type: "text",
					name: "state",
				}
			},
			{
				placeholder: "Country",
				src: "",
				dest: "client.address.country",
				required: true,
				validate: {
					type: "text",
					min: 3,
				},
				form: {
					type: "text",
					name: "country",
				}
			},
			{
				placeholder: "Zipcode",
				src: "",
				dest: "client.address.zipcode",
				required: true,
				validate: {
					type: "number",
					min: 5,
					max: 6,
				},
				form: {
					type: "number",
					name: "zipcode",
				}
			},
		],
		buttons: [
			{
				label: "Back",
				class: "btn btn-default",
				script: "back"
			},
			{
				label: "Checkout",
				class: "btn btn-success",
				script: "next"

			},
		],
		title: "Address",
		text: "",
		error: "",
		step: 1,
	},
	{
		data: [
			{
				placeholder: "Name on card",
				src: "",
				dest: "payment.name",
				required: true,
				validate: {
					type: "text",
					min: 3,
				},
				form: {
					type: "text",
					name: "ccname",
				}
			},
			{
				placeholder: "Card Number",
				src: "",
				dest: "payment.number",
				required: true,
				validate: {
					type: "creditcard",
					min: 10,
				},
				form: {
					type: "text",
					name: "ccnumber",
				}
			},
			{
				placeholder: "Expiration",
				src: "",
				dest: "payment.expiration",
				required: true,
				validate: {
					type: "date",
				},
				form: {
					type: "date",
					name: "ccexpiration",
				}
			},
			{
				placeholder: "CVV",
				src: "",
				dest: "payment.cvv",
				required: true,
				validate: {
					type: "number",
					min: 3,
					max: 3,
				},
				form: {
					type: "number",
					name: "ccvv",
				}
			},
		],
		buttons: [
			{
				label: "Back",
				class: "btn btn-default",
				script: "back"
			},
			{
				label: "Review",
				class: "btn btn-success",
				script: "next"
			},
		],
		title: "Payment",
		text: "Please select your preferred payment option and fill out the fields to finalize your purchase.",
		error: "",
		step: 1,
	},
]

const state = {
	steps: STEPS,
	products: {},
	current_item: {},
	current_form_step: 0,
}

const mutations = {
	[TYPE.ADD_PRODUCT]: (state, payload) => {
		state.products[payload.sku] = payload.data
	},
	[TYPE.SET_CURRENT_ITEM]: (state, payload) => {
		state.current_item = payload
	},
	[TYPE.SET_CURRENT_ITEM_PROP]: (state, payload) => {
		state.current_item[payload.prop] = payload.data
	},
	[TYPE.SET_CURRENT_FORM_STEP]: (state, value) => {
		state.current_form_step = value
	}
}

const actions = {
	addProduct({commit}, payload) {
		commit(TYPE.ADD_PRODUCT, payload)
	},
	setCurrentItem({commit}, payload) {
		commit(TYPE.SET_CURRENT_ITEM, payload)
	},
	setCurrentItemProp({commit}, payload) {
		commit(TYPE.SET_CURRENT_ITEM_PROP, payload)
	},
	setCurrentFormStep({commit}, value) {
		commit(TYPE.SET_CURRENT_FORM_STEP, value)
	}
}

const getters = {
	getCurrentFormStep: state => state.current_form_step,
	getFormSteps: state => state.steps,
	getProduct: state => sku => state.product[sku],
	getAllProducts: state => state.product,
	getCurrentItem: state => state.current_item,
	getCurrentItemProp: state => prop => state.current_item[prop],
}

export default {
	state,
	getters,
	mutations,
	actions
}