import React from 'react';
import PlacesAutocomplete, {geocodeByAddress, getLatLng,} from 'react-places-autocomplete';
import {withStyles} from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import Grid from '@material-ui/core/Grid';
import {geolocated} from "react-geolocated";
import History from "../../history"
import TextField from "@material-ui/core/TextField";
import DateTimePicker from 'react-datetime-picker';
import axios from "axios";
import moment from "moment";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import 'bootstrap/dist/css/bootstrap.css';

axios.defaults.baseURL = "https://backend.rmitassignment.tk/";


const styles = theme => ({
	root: {
		flexGrow: 1,
	},
	menuButton: {
		marginRight: theme.spacing(2),
	},
	title: {
		flexGrow: 1,
	},
});


class Profile extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			imageURL: "",
			file: null,
			files: [],
			imageStatus: false,
			address: '',
			updateaddress: '',
			lat: '',
			lng: '',
			Updatelat: '',
			Updatelng: '',
			originalLat: "",
			originalLng: "",
			FullAddress: "",
			UpdateFullAddress: "",
			userEmail: " ",
			useraddress: " ",
			Temp:"",
			profilePicture:"",
			date: new Date(),
			userid:"",
			schedules:[],
			displayAddress: false
		};
	}

	componentDidMount() {
		this.setState({userData: JSON.parse(localStorage.getItem("User_Info"))})
		console.log(this.state.userData);
	}

	componentWillReceiveProps(nextProps, nextContext) {
		console.log(nextProps.coords)
		if(nextProps.coords !== null){
			const post = {
				lat: nextProps.coords.latitude,
				lon: nextProps.coords.longitude
			};
			this.callAPI(post);
		}
		else {
			alert("Please Turn ON Location Services")
		}
		}

	handleChange = address => {
		this.setState({address});
	};

	handleSelect = async (address) => {
		let result = await geocodeByAddress(address)
		this.setState({FullAddress: result[0].formatted_address})
		let latlng = await getLatLng(result[0])
		console.log(latlng)
		this.setState({lat: latlng.lat, lng: latlng.lng})
	};

	handleChangeUpdate = updateaddress => {
		this.setState({updateaddress});
	};

	handleSelectUpdate = async (updateaddress) => {
		let result = await geocodeByAddress(updateaddress)
		this.setState({UpdateFullAddress: result[0].formatted_address})
		let latlng = await getLatLng(result[0])
		console.log(latlng)
		this.setState({Updatelat: latlng.lat, Updatelng: latlng.lng})
	};

	handleFileUpload = (event, ind) => {
		this.setState({file: event.target.files});
		this.submitFile(event.target.files, ind);
	};

	submitFile = (File, ind) => {
		let userInfo = JSON.parse(localStorage.getItem("User_Info"))
		let accessToken = userInfo.access_token;

		fetch("https://userprofilepicture.s3.amazonaws.com/"+File[0].name, {
				method: "PUT",
				cors:"no-cors",
				body: File[0]
			}).then(response => response)
				.then(data => {
					console.log(data)

					fetch("https://backend.rmitassignment.tk/weather/profile_picture",{
						method:"POST",
						cors:"no-cors",
						headers: {
							"x-api-key": "oN7aUdE07f7QEmIdbUnHr94Jo8kbijFb5esoeXbH",
							"content-type": "application/json",
							"Authorization": accessToken
						},
						body: JSON.stringify({
							filename: File[0].name,
						})

					}).then(res=> res.json()).then(data => {
						console.log(data);
						window.location.reload();
					})
				});

	};

	callAPI(post) {
		let userInfo = JSON.parse(localStorage.getItem("User_Info"))
		let accessToken = userInfo.access_token;

		fetch("https://backend.rmitassignment.tk/weather/dashboard", {
			method: "POST",
			cors:"no-cors",
			headers: {
				"x-api-key": "oN7aUdE07f7QEmIdbUnHr94Jo8kbijFb5esoeXbH",
				"content-type": "application/json",
				"Authorization": accessToken
			},
			body: JSON.stringify({
				lat: post.lat.toString(),
				lon: post.lon.toString(),
			})
		}).then(response => response.json())
			.then(data => {
				this.setState({
					userEmail: data.data.user.email,
					useraddress: data.data.user.address,
					profilePicture:data.data.user.profile_picture,
					userid: data.data.user.user_id,
					schedules: data.data.schedules
				})


				data.data.temperature.data.map((result)=>{
					this.setState({Temp: result.temp})
				})

			});
	}

	onChange = date => this.setState({ date })

	logout = e => {
		localStorage.removeItem("User_Info");
		localStorage.removeItem("RememberMe");
		History.push("/")
		window.location.reload()
	};

	addSchedule = (date,lat, lng, address) => {
		var n = date.toUTCString();
		var ts = moment(n).valueOf();
		var epochseconds = ts/1000;

		let userInfo = JSON.parse(localStorage.getItem("User_Info"))
		let accessToken = userInfo.access_token;

		fetch("https://backend.rmitassignment.tk/weather/add_schedule", {
			method: "POST",
			cors:"no-cors",
			headers: {
				"x-api-key": "oN7aUdE07f7QEmIdbUnHr94Jo8kbijFb5esoeXbH",
				"content-type": "application/json",
				"Authorization": accessToken
			},
			body: JSON.stringify({
				notification_time: epochseconds,
				lat: lat.toString(),
				lon: lng.toString(),
				area:address
			})
		}).then(response => response.json())
			.then(data => {
				console.log(data)
				window.location.reload();
			});
	}

	deleteSchedule = (scheduleID) => {

		let userInfo = JSON.parse(localStorage.getItem("User_Info"))
		let accessToken = userInfo.access_token;

		var raw = "";
		var requestOptions = {
			method: 'DELETE',
			cors:"no-cors",
			headers: {
			"x-api-key": "oN7aUdE07f7QEmIdbUnHr94Jo8kbijFb5esoeXbH",
				"content-type": "application/json",
				"Authorization": accessToken
		},
			body: raw,
			redirect: 'follow'
		};

		fetch("https://backend.rmitassignment.tk/weather/delete_schedule?schedule_id="+scheduleID, requestOptions)
			.then(response => response.text())
			.then(result => {
				console.log(result);
				window.location.reload();
			})
			.catch(error => console.log('error', error));
	}

	updateuser = (address) => {
		let userInfo = JSON.parse(localStorage.getItem("User_Info"))
		let accessToken = userInfo.access_token;


		fetch("https://backend.rmitassignment.tk/user/update", {
			method: "PUT",
			cors:"no-cors",
			headers: {
				"x-api-key": "oN7aUdE07f7QEmIdbUnHr94Jo8kbijFb5esoeXbH",
				"content-type": "application/json",
				"Authorization": accessToken
			},
			body: JSON.stringify({
				user_id: this.state.userid,
				address: address,
			})
		}).then(response => response.json())
			.then(data => {
				console.log(data);
				window.location.reload();
			});
	}

	updateSchedule = () =>{
		let userInfo = JSON.parse(localStorage.getItem("User_Info"))
		let accessToken = userInfo.access_token;


		fetch("https://backend.rmitassignment.tk/weather/update_schedule", {
			method: "PUT",
			cors:"no-cors",
			headers: {
				"x-api-key": "oN7aUdE07f7QEmIdbUnHr94Jo8kbijFb5esoeXbH",
				"content-type": "application/json",
				"Authorization": accessToken
			},
			body: JSON.stringify({
				schedule_id: '',
				notification_time: '',
				lat: '',
				lon: '',
			})
		}).then(response => response.json())
			.then(data => {
				console.log(data);
				window.location.reload();
			});
	}

	showAddress=()=>{
		this.setState({displayAddress:true})
	}

	render() {
// style={{backgroundColor:"#f2fff5"}}
		// style={{backgroundColor:"#e1eef0"}}
		const {classes} = this.props;
		return (
			<div>
				<AppBar position="static">
					<Toolbar>
						<IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">

						</IconButton>
						<Typography variant="h6" className={classes.title}>
							WeatherZone
						</Typography>
						<Button color="inherit" onClick={this.logout}>Log Out</Button>
					</Toolbar>
				</AppBar>
				{
					this.state.userEmail === " "?<p style={{textAlign:"center"}}><strong>Loading...</strong></p>:
					<table className="table">
					<thead>
					<tr style={{backgroundColor:"#f2fff5"}}>
						<td style={{textAlign:"center"}}>
							<p><strong>Hello,</strong> {this.state.userEmail}</p><br/>
							{this.state.profilePicture === null ? <div>
								<img
									src="https://userprofilepicture.s3-ap-southeast-2.amazonaws.com/nouser.png"
									alt=""
									style={{
										height: "150px",
										width: "150px",
									}}
								/>
								<form>
									<small>Upload Profile Picture</small><br/>
									<input label='Choose File Here' type='file' accept="image/*"
									       onChange={(e) => this.handleFileUpload(e, 1)}/>
								</form>
							</div> : <div>
								<img
									src={this.state.profilePicture}
									alt=""
									style={{
										height: "150px",
										width: "150px",
									}}
								/>
								<form>
									<small>Upload Profile Picture</small><br/>
									<input label='Upload Profile Picture' type='file' accept="image/*"
									       onChange={(e) => this.handleFileUpload(e, 1)}/>
								</form>
								<img
									src={this.state.imageURL}
									alt=""
									style={{
										height: "500px",
										width: "500px",
									}}
								/>
							</div>}
						</td>
						<td style={{textAlign:"center"}}>
							<p>Temperature: <strong>{this.state.Temp}</strong> Celcius<small>(Based on your IP)</small></p><br/>
							<p>Your Address: <strong>{this.state.useraddress}</strong></p><br/>
							<button onClick={this.showAddress}>Change Address</button>

							{this.state.displayAddress?<div><PlacesAutocomplete value={this.state.updateaddress}
							                                                    onChange={this.handleChangeUpdate}
							                                                    onSelect={this.handleSelectUpdate}>
								{({getInputProps, suggestions, getSuggestionItemProps, loading}) => (
									<div>

										<TextField variant="outlined"
										           margin="normal"
										           required
										           {...getInputProps({
											           placeholder: 'Type Address',
											           className: 'location-search-input',
										           })}
										/>
										<div className="autocomplete-dropdown-container" style={{marginLeft:"25%"}}>
											{loading && <div>Loading...</div>}
											{suggestions.map(suggestion => {
												const className = suggestion.active
													? 'suggestion-item--active'
													: 'suggestion-item';
												// inline style for demonstration purpose
												const style = suggestion.active
													? {width: "300px", backgroundColor: '#a3a3a3', cursor: 'pointer'}
													: {width: "300px", backgroundColor: '#ffffff', cursor: 'pointer'};
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
								{this.state.UpdateFullAddress === '' ? "" : <div>
									<p>{this.state.UpdateFullAddress}&nbsp;Latitude:<strong>{this.state.Updatelat}</strong>&nbsp;Longitude:<strong>{this.state.Updatelng}</strong></p>
									<button onClick={() => {
										this.updateuser(this.state.UpdateFullAddress)
									}}>Update
									</button>
								</div>}</div>:""}
						</td>
					</tr>
					<tr style={{backgroundColor:"#e1eef0"}}>
						<td style={{textAlign: 'center'}}>
							<PlacesAutocomplete value={this.state.address}
							                    onChange={this.handleChange}
							                    onSelect={this.handleSelect}>
								{({getInputProps, suggestions, getSuggestionItemProps, loading}) => (
									<div>
										<h3>Get instant notification about weather</h3>
										<TextField variant="outlined"
											// margin="normal"
											         label="Type Address"
											         required
											         {...getInputProps({
												         placeholder: 'Type Address',
												         className: 'location-search-input',
											         })}
										/>
										<div className="autocomplete-dropdown-container" style={{marginLeft: "25%"}}>
											{loading && <div style={{marginLeft: "-25%"}}>Loading...</div>}
											{suggestions.map(suggestion => {
												const className = suggestion.active
													? 'suggestion-item--active'
													: 'suggestion-item';
												// inline style for demonstration purpose
												const style = suggestion.active
													? {width: "300px", backgroundColor: '#a3a3a3', cursor: 'pointer'}
													: {width: "300px", backgroundColor: '#ffffff', cursor: 'pointer'};
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
							{this.state.FullAddress === '' ? "" : <div>
								<p>{this.state.FullAddress}&nbsp;Latitude:<strong>{this.state.lat}</strong>&nbsp;Longitude:<strong>{this.state.lng}</strong></p>
							</div>}
							{this.state.lng === '' ? "" :
								<div>
									<h5>Select Date/Time</h5>
									<DateTimePicker
										onChange={this.onChange}
										value={this.state.date}
									/>
								</div>}
							{this.state.lng === '' ?
								<div>
									<br/>
									<br/>
									<br/>
									<br/>
									<br/>
									<br/>
								</div> : <button onClick={() => {
								this.addSchedule(this.state.date, this.state.lat, this.state.lng,this.state.FullAddress)
							}}>Get Notification</button>}



						</td>
						<td style={{textAlign: 'center'}}>
							<h3 style={{textAlign: 'center'}}>Your upcoming notification</h3>
							<TableContainer component={Paper}>
								<Table className={classes.table} style={{ backgroundColor:"#e6ffe0"}} aria-label="simple table">
									<TableHead>
										<TableRow>
											<TableCell style={{border: "1px dotted grey"}} align="center">Area</TableCell>
											<TableCell style={{border: "1px dotted grey"}} align="center">Time</TableCell>
											<TableCell style={{border: "1px dotted grey"}} align="center">Delete</TableCell>
										</TableRow>
									</TableHead>
									<TableBody>
										{this.state.schedules.map((row) => (
											<TableRow key={row.schedule_id}>
												<TableCell style={{border: "1px dotted grey"}} align="center">{row.area}</TableCell>
												<TableCell style={{border: "1px dotted grey"}}
												           align="center">{String(new Date(row.notification_time * 1000)).replace("GMT+0500 (Pakistan Standard Time)", " ")}</TableCell>
												<TableCell style={{border: "1px dotted grey"}} align="center"><button onClick={() => {
													this.deleteSchedule(row.schedule_id)
												}}>Delete</button></TableCell>
											</TableRow>
										))}
									</TableBody>
								</Table>
							</TableContainer>
						</td>
					</tr>
					</thead>
				</table>
				}
			</div>
		)
	}
}




export default geolocated({
	positionOptions: {
		enableHighAccuracy: false,
	},
	userDecisionTimeout: 5000,
})(withStyles(styles)(Profile));

