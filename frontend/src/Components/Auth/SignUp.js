import React, {Component} from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import {connect} from "react-redux";
import {SignUpAction} from "./SignUpAction";
import {withStyles} from "@material-ui/core/styles";
//import CircularLoader from "../Loader/circularLoader";
import {Alert} from '@material-ui/lab';


import Paper from '@material-ui/core/Paper';
import PlacesAutocomplete, {geocodeByAddress, getLatLng} from "react-places-autocomplete";


const styles = theme => ({
	root: {
		height: '100vh',
	},
	image: {
		backgroundImage: 'url(https://source.unsplash.com/random)',
		backgroundRepeat: 'no-repeat',
		backgroundColor:
			theme.palette.type === 'light' ? theme.palette.grey[50] : theme.palette.grey[900],
		backgroundSize: 'cover',
		backgroundPosition: 'center',
	},
	paper: {
		margin: theme.spacing(8, 4),
		display: 'flex',
		flexDirection: 'column',
		alignItems: 'center',
	},
	avatar: {
		margin: theme.spacing(1),
		backgroundColor: theme.palette.secondary.main,
	},
	form: {
		width: '100%', // Fix IE 11 issue.
		marginTop: theme.spacing(1),
	},
	submit: {
		margin: theme.spacing(3, 0, 2),
	},
});

class SignUp extends Component {
	constructor(props) {
		super(props);
		this.state = {
			loader: false,
			email: '',
			message: '',
			password: '',
			address:'',
			error: false,
			rememberme: false,
			lat:'',
			lng: '',
			FullAddress:"",

		};
		this.handleChangeText = this.handleChangeText.bind(this);
		this.handleError = this.handleError.bind(this);

	}

	handleChangeText = e => {
		this.setState({[e.target.name]: e.target.value});
		if (e.target.checked) {
			localStorage.setItem("RememberMe", e.target.checked);
		}
	};

	componentDidMount(nextProps) {
		localStorage.getItem("User_Info") !== null && localStorage.getItem("RememberMe") === "true" ? this.props.history.push("/home") : console.log()
	}

	componentWillReceiveProps(nextProps, nextContext) {
		if (nextProps.LoginState !== "") {
			this.setState({loader: false});
			this.setState({error: true});
			this.setState({message: nextProps.LoginState});
		}
	}

	handleChange = address => {
		this.setState({ address });
	};

	handleSelect = async (address) => {
		let result = await geocodeByAddress(address)
		this.setState({FullAddress: result[0].formatted_address})
		let latlng = await getLatLng(result[0])
		console.log(latlng)
		this.setState({lat: latlng.lat, lng:latlng.lng})
	};



	onSubmit = e => {
		e.preventDefault();
		// history.push("/admin")
		if (this.state.email === "" || this.state.password === "" || this.state.FullAddress === "") {
			this.setState({message: "Please fill All Required Properties"});
			this.setState({error: true})
		} else {
			const post = {
				email: this.state.email,
				password: this.state.password,
				address: this.state.FullAddress
			};
			console.log(this.props.history)
			debugger;
			this.props.SignUpAction(post, this.props.history);
			this.setState({loader: true})
		}

	};
	handleError = e => {
		this.setState({error: false})
	};

	openSignIn = () => {
		this.props.history.push("/")
	}

	render() {
		const {classes} = this.props;
		return (


			<Grid container component="main" className={classes.root}>
				<CssBaseline/>

				<Grid item xs={12} sm={6} md={6} component={Paper} elevation={6} square>
					<div className={classes.paper}>
						{this.state.error && (
							<Alert severity="error" onClose={this.handleError}>{this.state.message}</Alert>
						)}
						<Avatar className={classes.avatar}>
							<LockOutlinedIcon/>
						</Avatar>
						<Typography component="h1" variant="h5">
							Sign Up
						</Typography>
						<form className={classes.form} noValidate>


							<TextField
								onChange={this.handleChangeText}
								variant="outlined"
								margin="normal"
								required
								fullWidth
								id="email"
								label="Email Address"
								name="email"
								autoComplete="email"
								autoFocus
								value={this.state.email}
							/>
							<TextField
								onChange={this.handleChangeText}
								variant="outlined"
								margin="normal"
								required
								fullWidth
								name="password"
								label="Password"
								type="password"
								id="password"
								autoComplete="current-password"
								value={this.state.password}
							/>

							<PlacesAutocomplete  value={this.state.address}
							                     onChange={this.handleChange}
							                     onSelect={this.handleSelect}>
								{({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
									<div>

										<TextField variant="outlined"
										           margin="normal"
										           required
										           fullWidth
											{...getInputProps({
												placeholder: 'Type Address',
												className: 'location-search-input',
											})}
										/>
										<div className="autocomplete-dropdown-container">
											{loading && <div>Loading...</div>}
											{suggestions.map(suggestion => {
												const className = suggestion.active
													? 'suggestion-item--active'
													: 'suggestion-item';
												// inline style for demonstration purpose
												const style = suggestion.active
													? { width:"300px",backgroundColor: 'pink', cursor: 'pointer' }
													: { width:"300px",backgroundColor: '#ffffff', cursor: 'pointer' };
												return (
													<div
														{...getSuggestionItemProps(suggestion, {
															className,
															style,
														})}
													>
														<span>{suggestion.description}</span>
													</div>
												);
											})}
										</div>
									</div>
								)}

							</PlacesAutocomplete>
							<h5>{this.state.FullAddress}</h5>

							<Button
								type="submit"
								fullWidth
								variant="contained"
								color="primary"
								className={classes.submit}
								onClick={this.onSubmit}
							>
								Sign Up
							</Button>
							<Grid container>
								<Grid item xs>

								</Grid>
								<Grid item>
									<Link variant="body2" onClick={this.openSignIn}>
										{"Already have an account? Sign in"}
									</Link>
								</Grid>
							</Grid>
						</form>
					</div>
				</Grid>
				<Grid item xs={false} sm={6} md={6}  component={Paper} elevation={6} square>
					<img
						src="https://userprofilepicture.s3-ap-southeast-2.amazonaws.com/background.png"
						alt=""
						style={{
							height: "100%",
							width: "100%",
						}}
					/>
				</Grid>
			</Grid>
		);
	}
}

const mapStateToProps = state => ({
	LoginState: state.signUp.login_Failed,
});


export default connect(
	mapStateToProps,
	{SignUpAction}
)(withStyles(styles)(SignUp));











