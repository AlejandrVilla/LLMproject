import axios from "axios";
import React, { useState } from "react";
import { Link } from "react-router-dom";
import './forms.scss'

const SIGNUP_URL = "http://127.0.0.1:5006/signup/"

function Signup(){
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [name, setName] = useState("");
    const [lastName, setLastName] = useState("");

    const registerUser = async (e) => {
        e.preventDefault();
        try{
            const response = await axios.post(
                SIGNUP_URL, {
                    username: username,
                    email: email,
                    password: password,
                    name: name,
                    last_name: lastName
                }, {
                    headers: { 'Request-type': 'sign up' },
                    withCredentials: true
                }
            );

            const data = response.data
            const headers = response.headers
            console.log(data);
            console.log(headers);
            window.location.href = "/";
        }catch (error){
            if (error.response.status === 409){
                alert("invalid credentials");
            }
            console.error('Error: ', error)
        }
    }

    return(
        <div className="signup-div">
            <h1 className="singup-title">Create an account</h1>
            <form className="signup-form" onSubmit={registerUser}>
                <div className="user-signup-div">
                    <div className="user-info-div">
                        <div>
                            <input 
                                type="text" 
                                name="firstName" 
                                placeholder="First name" 
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                required/>
                        </div>
                        <div>
                            <input 
                                type="text" 
                                name="lastName" 
                                placeholder="Last name" 
                                value={lastName}
                                onChange={(e) => setLastName(e.target.value)}
                                required/>
                        </div>
                        <div>
                            <input 
                                type="email" 
                                name="email" 
                                placeholder="email@yourdomain.com" 
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required/>
                        </div>
                    </div>
                    <div className="user-credentials-div">
                        <div>
                            <input 
                                type="username" 
                                name="username" 
                                placeholder="Username" 
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                required/>
                        </div>
                        <div>
                            <input 
                                type="password" 
                                name="password" 
                                placeholder="Password" 
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required/>
                        </div>
                        <div>
                            <input 
                                type="password" 
                                name="confirmpassword" 
                                placeholder="Confirm Password" 
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required/>
                        </div>
                    </div>
                </div>
                <div className="signup-button-div">
                    <button className="signup-button" type="submit">Create</button>
                </div>
            </form>
            <div className="signup-footer">
                <p>Already have an account?</p>
                <Link className="signup-link" to={'/login'}>log in</Link>
            </div>
        </div>
    )
}

export { Signup };