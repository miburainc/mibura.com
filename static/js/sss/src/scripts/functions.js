import { forEachValue } from './util'

export function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function validatePhone(phone) {
	return /^(?:(?:\(?(?:00|\+)([1-4]\d\d|[1-9]\d?)\)?)?[\-\.\ \\\/]?)?((?:\(?\d{1,}\)?[\-\.\ \\\/]?){0,})(?:[\-\.\ \\\/]?(?:#|ext\.?|extension|x)[\-\.\ \\\/]?(\d+))?$/i.test(phone)
}

function setError(key, value) {

}

export function ValidateFormSteps(current_form, form_steps) {
	let errors = {
		valid: true,
		errors: {}
	}

	for (let i=0; i<form_steps.length; i++) {
		let current_form_item = current_form[form_steps[i].form.name]

		if (form_steps[i].required) {
			errors.errors[form_steps[i].form.name] = []
			console.log(current_form_item)

			if (current_form_item == undefined || current_form_item == "") {
				errors["valid"] = false
				errors.errors[form_steps[i].form.name].push("This field is required.")
			}
			else if (form_steps[i].validate) {

				forEachValue(form_steps[i].validate, (value, key) => {
					switch(key) {
						case "type":
							let valid = false;
							console.log("Validate Type")
							switch (value) {
								case "text":
									valid = /^\w+( \w+)*$/.test(current_form_item)
									break;
								case "number":
									valid = /^\d+$/.test(current_form_item);
									break;
								case "email":
									valid = validateEmail(current_form_item)
									break;
								case "phone":
									valid = validatePhone(current_form_item)
									break;
							}
							if (!valid) {
								errors["valid"] = false
								errors.errors[form_steps[i].form.name].push("The contents of this form field are invalid.")
							}
							break;
						case "min":
							console.log("Validate Length Min")
							if (current_form_item.length > parseInt(value)) {
								valid = true
							}
							else {
								errors["valid"] = false
								errors.errors[form_steps[i].form.name].push("Minimum length required is " + value + " characters.")
								valid = false
							}
							break;
						case "max":
							console.log("Validate Length Max")
							if (current_form_item.length < parseInt(value)) {
								valid = true
							}
							else {
								errors["valid"] = false
								errors.errors[form_steps[i].form.name].push("Maximum length required is " + value + " characters.")
								valid = false
							}
							break;
					}
				})
			}
		}	
	}
	return errors
}

