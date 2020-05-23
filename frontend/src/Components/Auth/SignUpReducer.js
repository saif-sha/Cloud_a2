const initialState = {
	items: [],
	login_Failed: "",
};

export default function (state = initialState, action) {
	switch (action.type) {
		case "SIGNUP_SUCCESS": {
			return {
				...state,
				items: action.payload
			};
		}
		case "SIGNUP_FAIL": {
			return {
				...state,
				login_Failed: action.payload.data.error.message
			};

		}
		default:
			return state;
	}
}
