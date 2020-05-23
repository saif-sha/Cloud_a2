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
import {SignInAction} from "./LoginAction";
import {withStyles} from "@material-ui/core/styles";
import Container from '@material-ui/core/Container';
//import CircularLoader from "../Loader/circularLoader";
import {Alert} from '@material-ui/lab';



import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';



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

class Login extends Component {
	constructor(props) {
		super(props);
		this.state = {
			loader: false,
			email: '',
			message: '',
			password: '',
			error: false,
			rememberme: false

		};
		this.handleChange = this.handleChange.bind(this);
		this.handleError = this.handleError.bind(this);

	}

	handleChange = e => {
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


	onSubmit = e => {
		e.preventDefault();
		// history.push("/admin")
		if (this.state.email === "" || this.state.password === "") {
			this.setState({message: "Please fill All Required Properties"});
			this.setState({error: true})
		} else {
			const post = {
				email: this.state.email,
				password: this.state.password
			};
			this.props.SignInAction(post, this.props.history);
			this.setState({loader: true})
		}

	};

	handleError = e => {
		this.setState({error: false})
	};

	openSignUp = () => {
		this.props.history.push("/signup")
	}
	render() {
		const {classes} = this.props;
		return (


			<Grid container component="main" className={classes.root}>
				<CssBaseline />

				<Grid item xs={12} sm={6} md={6} component={Paper} elevation={6} square>
					<div className={classes.paper}>
						{this.state.error && (
							<Alert severity="error" onClose={this.handleError}>{this.state.message}</Alert>
						)}
						<Avatar className={classes.avatar}>
							<LockOutlinedIcon />
						</Avatar>
						<Typography component="h1" variant="h5">
							Sign in
						</Typography>
						<form className={classes.form} noValidate>
							<TextField
								onChange={this.handleChange}
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
								onChange={this.handleChange}
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
							<FormControlLabel
								control={<Checkbox onChange={this.handleChange} value={this.state.rememberme} color="primary"/>}
								label="Remember me"
							/>
							<Button
								type="submit"
								fullWidth
								variant="contained"
								color="primary"
								className={classes.submit}
								onClick={this.onSubmit}
							>
								Sign In
							</Button>
							<Grid container>
								<Grid item xs>
									{/*<Link href="#" variant="body2">*/}
									{/*	Forgot password?*/}
									{/*</Link>*/}
								</Grid>
								<Grid item>
									<Link variant="body2" onClick={this.openSignUp}>
										{"Don't have an account? Sign Up"}
									</Link>
								</Grid>
							</Grid>
						</form>
					</div>
				</Grid>
				<Grid item xs={false} sm={6} md={6} component={Paper} elevation={6} square>
					{/*<div className={classes.paper}>*/}
						<img
							src="https://userprofilepicture.s3-ap-southeast-2.amazonaws.com/background.png"
							alt=""
							style={{
								height: "100%",
								width: "100%",
							}}
						/>

						{/*<h1>Cloud Computing Assignment 2</h1>*/}
					{/*	<br/><br/><br/>*/}
					{/*<h3>Developed By </h3>*/}
					{/*<h4>S3536400 - Mohammed Saif Shahid</h4>*/}
					{/*<h4>S3778229 - Ansar Ahmad</h4>*/}
					{/*</div>*/}
				</Grid>
			</Grid>
		);
	}
}

const mapStateToProps = state => ({
	LoginState: state.auth.login_Failed,
});


export default connect(
	mapStateToProps,
	{SignInAction}
)(withStyles(styles)(Login));

