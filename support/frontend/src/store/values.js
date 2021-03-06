if (window.SET_URL_ROOT == undefined) {
	window.SET_URL_ROOT = false
}
if (SET_API_ROOT == undefined) {
	var SET_API_ROOT = false
}



export var URL_ROOT = window.SET_URL_ROOT ? window.SET_URL_ROOT : "http://localhost:8000/"
export var API_ROOT = window.SET_API_ROOT ? window.SET_API_ROOT : "http://localhost:8000/support/api/"

export const PLANS = [
	{
		code: "silver",
		name: "Silver Pro",
		cost: 49,
		color: "linear-gradient(90deg,rgba(170,170,170,1) 0%,rgba(213,213,213,1) 100%)"
	},
	{
		code: "gold",
		name: "Pure Gold",
		cost: 99,
		// color: "#f6d579",
		color: "linear-gradient(90deg,rgba(242,213,134,1) 0%,rgba(227,193,96,1) 100%)"
	},
	{
		code: "black",
		name: "Carbon Black",
		cost: 499,
		color: '#000000',
		// color: "repeating-linear-gradient(-26deg, rgba(255,255,255, 0.02), rgba(255,255,255, 0.12) 2px, transparent 3px, transparent 7px)"
	},
]


// Product multiplier every 6 months

// Product price =
// plan_price * ( product.category.start_value * (1+increment) )
// yearly compound ??

export const step_names = {
	start: 0,
	item: 1,
	cloud: 2,
	client_info: 3,
	client_address: 4,
	payment: 5,
	checkout: 6,
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
	{	//start screen
		data: [
			
		],
		buttons: [
			{
				label: "I'm a new customer",
				class: "btn btn-lg btn-outline-success",
				script: "next"
			},
			{
				label: "I'm ready to pay for an existing quote",
				class: "btn btn-lg btn-outline-default",
				script: "pay"
			}
		],
		title: "",
		text: "",
		error: "",
		step: 0,
		buttonStyle: "text-align: center; margin-top: 12px;"
	},
	{	//item
		data: [
			{
				placeholder: "Product Name",
				src: "item",
				dest: "cart.#.brand",
				required: true,
				form: {
					type: "text",
					name: "model",
				},
				validate: {
					type: "text",
					min: 2,
				}
			},
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
			}
		],
		buttons: [
			{
				label: "Back",
				class: "btn btn-lg btn-outline-default",
				script: "back"
			},
			{
				label: "Add another",
				class: "btn btn-lg btn-outline-success",
				script: "start,additem"

			},
			{
				label: "Add and Continue",
				class: "btn btn-lg btn-outline-success",
				script: "next,additem"

			},
		],
		title: "Item",
		text: "Please type the brand or model of your item",
		error: "We aren't sure if we support this brand or model.  Please check the spelling, or contact us to find out if we can support it!",
		step: 0,
		buttonStyle: "margin-top: 14px;"
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
				label: "I Don't Need Cloud Support",
				class: "btn btn-lg btn-outline-default",
				script: "skip"

			},
			{
				label: "Add and Continue",
				class: "btn btn-lg btn-outline-success",
				script: "addcloud"

			},
		],
		title: "Cloud Provider",
		text: "Add a cloud provider",
		error: "",
		step: 1,
		buttonStyle: "text-align: center; margin-top: 50px;"
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
				label: "Back",
				class: "btn btn-lg btn-outline-default",
				script: "back"
			},
			{
				label: "Continue",
				class: "btn btn-lg btn-outline-success",
				script: "next"

			},
		],
		title: "Personal Information",
		text: "",
		error: "",
		step: 2,
		buttonStyle: "margin-top: 14px;"
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
				class: "btn btn-lg btn-outline-default",
				script: "back"
			},
			{
				label: "Continue to Payment",
				class: "btn btn-lg btn-outline-success",
				script: "next"

			},
		],
		title: "Address",
		text: "",
		error: "",
		step: 2,
		buttonStyle: "margin-top: 14px;"
	},
	{
		data: [
			
			
		],
		buttons: [
			{
				label: "Back",
				class: "btn btn-lg btn-outline-default",
				script: "back"
			},
			{
				label: "Review",
				class: "btn btn-lg btn-outline-success payment-button",
				script: "review"
			},
		],
		title: "Review",
		text: "",
		error: "",
		step: 3,
		buttonStyle: ""
	},
	{
		data: [
			{
				placeholder: "Name on card",
				src: "",
				dest: "payment.cardname",
				required: true,
				validate: {
					type: "text",
					min: 3,
				},
				form: {
					type: "text",
					name: "cardname",
					class: "field",
				}
			},
			{
				placeholder: "Cardholder Phone",
				src: "",
				dest: "payment.cardphone",
				required: true,
				validate: {
					type: "phone",
					min: 6,
				},
				form: {
					type: "tel",
					name: "cardphone",
					class: "field",
				}
			},
			{
				placeholder: "Company Name",
				src: "",
				dest: "payment.bankname",
				required: true,
				validate: {
					type: "text",
					min: 3,
				},
				form: {
					type: "text",
					name: "bankname",
					class: "field",
				}
			},
			{
				placeholder: "Phone Number",
				src: "",
				dest: "payment.bankphone",
				required: true,
				validate: {
					type: "phone",
					min: 6,
				},
				form: {
					type: "tel",
					name: "bankphone",
					class: "field",
				}
			}			
		],
		buttons: [
			{
				label: "Back",
				class: "btn btn-lg btn-outline-default",
				script: "back"
			},
			{
				label: "Review",
				class: "btn btn-lg btn-outline-success payment-button",
				script: "review"
			},
		],
		title: "Payment",
		text: "Please select your preferred payment option and fill out the fields to finalize your purchase.",
		error: "",
		step: 3,
		buttonStyle: ""
	}
]
