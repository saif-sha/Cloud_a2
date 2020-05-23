import React from 'react';
import './App.css';
import Login from "./Components/Auth/Login"
import Signup from "./Components/Auth/SignUp"
import Home from "./Components/Auth/Home"
import {BrowserRouter as Router, Route, Switch, Redirect} from "react-router-dom";
import "./App.css";
import history from './history';
// const PrivateRoute = ({ component: Component, ...rest }) => {
//
//   return (
//     <Route
//       {...rest}
//       render={props =>
//         localStorage.getItem("ACCESS-TOKEN") !== null
//           ? <Component {...props} />
//           : <Redirect
//             to={{
//               pathname: rest.path,
//             }}
//           />}
//     />);
// };

function App() {
  return (
    <Router history={history}>
      <Switch>
        <Route exact path="/" component={Login}/>
        <Route path="/signup" component={Signup}/>
        <Route path="/home" component={Home}/>
        <Route component={Login}/>

      </Switch>
    </Router>
  );
}

export default App;
