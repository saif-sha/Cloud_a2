const initialState = {
    data: [],
    logged_In: localStorage.getItem("ACCESS-TOKEN") !== null,
    login_Failed: "",
};

export default function (state = initialState, action) {
    switch (action.type) {
        case "LOGIN_SUCCESS": {
            return {
                ...state,
                data: action.payload.data.data
            };
        }
        case "LOGIN_FAIL": {
            return {
                ...state,
                login_Failed: action.payload.data.error.message
            };

        }
        default:
            return state;
    }
}
