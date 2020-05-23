import { combineReducers } from "redux";
import authReducers from "./Components/Auth/LoginReducer";
import signUpReducers from "./Components/Auth/SignUpReducer";

export default combineReducers({
	auth: authReducers,
	signUp: signUpReducers,
});
