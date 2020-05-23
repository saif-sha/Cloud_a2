import axios from "axios";

axios.defaults.baseURL = "https://backend.rmitassignment.tk/";


export const SignUpAction = (postData, history) => dispatch => {
	axios("user/signup", {
		method: "POST",
		headers: {
			"x-api-key": "oN7aUdE07f7QEmIdbUnHr94Jo8kbijFb5esoeXbH",
			"content-type": "application/json"
		},
		data: JSON.stringify(postData)
	}).then(post => {
		dispatch({
			type: "SIGNUP_SUCCESS",
			payload: post
		});
		history.push("/Login")
	}).catch(err => {
		dispatch({
			type: "SIGNUP_FAIL",
			payload: err.response
		});
	});
};
