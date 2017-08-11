console.log(window.SET_URL_ROOT)
console.log(window.SET_URL_ROOT == undefined)

if (window.SET_URL_ROOT == undefined) {
	window.SET_URL_ROOT = false
}
if (SET_API_ROOT == undefined) {
	var SET_API_ROOT = false
}



export var URL_ROOT = window.SET_URL_ROOT ? window.SET_URL_ROOT : "http://localhost:8000/"
export var API_ROOT = window.SET_API_ROOT ? window.SET_API_ROOT : "http://localhost:8000/support/api/"

console.log("URL_ROOT: " + URL_ROOT)
console.log("API_ROOT: " + API_ROOT)

export const PLANS = [
	{
		name: "Silver Pro",
		cost: 49,
		color: "#ebebeb"
	},
	{
		name: "Pure Gold",
		cost: 99,
		color: "#f4c730"
	},
	{
		name: "Carbon Black",
		cost: 499,
		color: "#000000"
	},
]


// Product multiplier every 6 months

// Product price =
// plan_price * ( product.category.start_value * (1+increment) )
// yearly compound ??

export const step_names = {
	brand: 0,
	model: 1,
	additional_info: 2,
	cloud: 3,
	client_info: 4,
	client_address: 5,
	payment: 6,
}

export const product_multiplier = {
	none: {
		start_value: 1.0, // multiplier on plan
		increment: 0.10, // 10% every 6 months
	},
	cloud: {
		start_value: 1.0, // multiplier on plan
		increment: 0.0, // 10% every 6 months
	},
	servers: {
		start_value: 1.0, // multiplier on plan
		increment: 0.10, // 10% every 6 months
	},
	storage: {
		start_value: 1.0, // multiplier on plan
		increment: 0.20, // 20% every 6 months
	},
	network: {
		start_value: 1.0, // multiplier on plan
		increment: 0.10, // 10% every 6 months
	},
	appliances: {
		start_value: 1.0, // multiplier on plan
		increment: 0.10, // 10% every 6 months
	},
}

export const form_steps = [
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
					min: 1,
				}
			},
		],
		buttons: [
			{
				label: "Next",
				class: "btn btn-outline-success",
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
				class: "btn btn-outline-default",
				script: "back"
			},
			{
				label: "Next",
				class: "btn btn-outline-success",
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
				required: true,
				form: {
					type: "text",
					name: "serialnumber"
				},
				validate: {
					min: 3
				},
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
				placeholder: "Additional Info",
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
				class: "btn btn-outline-default",
				script: "back"
			},
			{
				label: "Add Another",
				class: "btn btn-outline-default",
				script: "start,additem"
			},
			{
				label: "Add and Checkout",
				class: "btn btn-outline-success",
				script: "next,additem"

			},
		],
		title: "Additional Information",
		text: "",
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
				label: "Skip",
				class: "btn btn-outline-default",
				script: "skip"

			},
			{
				label: "Next",
				class: "btn btn-outline-success",
				script: "next,addcloud"

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
				class: "btn btn-outline-success",
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
				dest: "client.address.street2",
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
				class: "btn btn-outline-default",
				script: "back"
			},
			{
				label: "Checkout",
				class: "btn btn-outline-success",
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
					name: "cardholder-name",
					class: "field",
				}
			},
			{
				placeholder: "Cardholder Phone",
				src: "",
				dest: "payment.phone",
				required: true,
				validate: {
					type: "phone",
					min: 6,
				},
				form: {
					type: "tel",
					name: "ccphone",
					class: "field",
				}
			},
			{
				placeholder: "Card",
				src: "",
				dest: "payment.number",
				required: false,
				validate: {
					type: "text",
				},
				form: {
					type: "stripe",
					name: "ccnumber",
				}
			},
			
		],
		buttons: [
			{
				label: "Back",
				class: "btn btn-outline-default",
				script: "back"
			},
			{
				label: "Review",
				class: "btn btn-outline-success payment-button",
				script: "review"
			},
		],
		title: "Payment",
		text: "Please select your preferred payment option and fill out the fields to finalize your purchase.",
		error: "",
		step: 1,
	},
]
