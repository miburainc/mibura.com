import axios from 'axios'
import Cookies from 'js-cookie'



const csrf_token = Cookies.get('csrftoken')
// axios.defaults.headers.common["X-CSRFToken"] = csrf_token
// axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
// axios.defaults.xsrfCookieName = "csrftoken";
const ajax = axios.create({
	// `xsrfHeaderName` is the name of the http header that carries the xsrf token value
	// headers: {
		xsrfHeaderName: "X-CSRFTOKEN", // default
		xsrfCookieName: "csrftoken",
		// withCredentials: true,
		// credentials: 'same-origin',
	// }
});
export default ajax