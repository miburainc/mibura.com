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
	review: 5,
	payment: 6,
	verify: 7,
	success: 8
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
				label: "New Customer",
				class: "btn btn-lg btn-success",
				script: "next"
			},
			{
				label: "Already have a quote? Click here to checkout",
				class: "btn btn-lg btn-default",
				script: "returning"
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
				class: "btn btn-lg btn-default",
				script: "back"
			},
			{
				label: "Add",
				class: "btn btn-lg btn-success",
				script: "start,additem"

			},
			{
				label: "Add and Continue",
				class: "btn btn-lg btn-success",
				script: "next,additem"

			},
		],
		title: "On-Premise Hardware - Software",
		text: "Search for your hardware device or software below",
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

				label: "Skip",
				class: "btn btn-lg btn-default",
				script: "skip"

			},
			{
				label: "Add",
				class: "btn btn-lg btn-success",

				script: "addcloud"

			},
			{
				label: "Add and Continue",
				class: "btn btn-lg btn-outline-success",
				script: "addcloud,next"

			},
		],
		title: "Add Cloud Support",
		text: "If you have multiple cloud providers, please add and below tell us a little about your tenant(s)",
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
				class: "btn btn-lg btn-default",
				script: "back"
			},
			{
				label: "Continue",
				class: "btn btn-lg btn-success",
				script: "next"

			},
		],
		title: "About your company",
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
					min: 2,
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
				class: "btn btn-lg btn-default",
				script: "back"
			},
			{
				label: "Review Cart",
				class: "btn btn-lg btn-success",
				script: "next"

			},
		],
		title: "Billing Address",
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
				class: "btn btn-lg btn-default",
				script: "back"
			},
			{
				label: "Get Quote",
				class: "btn btn-lg btn-info",
				script: "getquote"
			},
			{
				label: "Checkout Now",
				class: "btn btn-lg btn-success payment-button",
				script: "gotocheckout"
			},
		],
		title: "Looks good?",
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
				placeholder: "Bank Customer Name",
				src: "",
				dest: "payment.bankcustomername",
				required: true,
				validate: {
					type: "text",
					min: 3,
				},
				form: {
					type: "text",
					name: "bankcustomername",
					class: "field",
				}
			},
			{
				placeholder: "Account Number",
				src: "",
				dest: "payment.accountnumber",
				required: true,
				validate: {
					type: "number",
					min: 6,
				},
				form: {
					type: "number",
					name: "accountnumber",
					class: "field",
				}
			},
			{
				placeholder: "Routing Number",
				src: "",
				dest: "payment.routingnumber",
				required: true,
				validate: {
					type: "number",
					min: 6,
				},
				form: {
					type: "number",
					name: "routingnumber",
					class: "field",
				}
			},
			{
				placeholder: "Verify Ammount #1",
				src: "",
				dest: "payment.verify1",
				required: true,
				validate: {
					type: "number",
					min: 2,
				},
				form: {
					type: "number",
					name: "verify1",
					class: "field",
				}
			},
			{
				placeholder: "Verify Ammount #2",
				src: "",
				dest: "payment.verify2",
				required: true,
				validate: {
					type: "number",
					min: 2,
				},
				form: {
					type: "number",
					name: "verify2",
					class: "field",
				}
			},
			{
				placeholder: "P.O. Number",
				src: "",
				dest: "payment.ponumber",
				required: true,
				validate: {
					type: "text",
					min: 4,
				},
				form: {
					type: "text",
					name: "ponumber",
					class: "field",
				}
			}			
		],
		buttons: [
			{
				label: "Back",
				class: "btn btn-lg btn-default",
				script: "back"
			},
			{
				label: "Continue",
				class: "btn btn-lg btn-success payment-button",
				script: "review"
			},
		],
		title: "Payment",
		text: "We accept all major credit cards, Bank ACH, or if you already have an account with Mibura, simply create a purchase order here",
		error: "",
		step: 3,
		buttonStyle: ""
	},
	{
		data: [
			
			
		],
		buttons: [
			{
				label: "Back",
				class: "btn btn-lg btn-default",
				script: "back"
			},
			{
				label: "Submit Payment",
				class: "btn btn-lg btn-success payment-button",
				script: "purchase"
			},
		],
		title: "Verify",
		text: "",
		error: "",
		step: 3,
		buttonStyle: ""
	},
	{
		data: [
			
			
		],
		buttons: [
			
		],
		title: "Success",
		text: "",
		error: "",
		step: 3,
		buttonStyle: ""
	}
]
