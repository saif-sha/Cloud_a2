import axios from "axios";

axios.defaults.baseURL = "https://backend.rmitassignment.tk/";


export const SignInAction = (postData, history) => dispatch => {
    axios("user/signin", {
        method: "POST",
        headers: {
            "x-api-key": "oN7aUdE07f7QEmIdbUnHr94Jo8kbijFb5esoeXbH",
            "content-type": "application/json"
        },
        data: JSON.stringify(postData)
    }).then(post => {
        dispatch({
            type: "LOGIN_SUCCESS",
            payload: post
        });
        localStorage.setItem("User_Info", JSON.stringify(post.data.data));
        history.push("/home")
    }).catch(err => {
        dispatch({
            type: "LOGIN_FAIL",
            payload: err.response
        });
    });
};
