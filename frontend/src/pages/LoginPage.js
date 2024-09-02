import axios from "axios";
import React, {useState} from "react";
import { Link } from "react-router-dom";
import './forms.scss'

const LOGIN_URL = "http://127.0.0.1:5006/login/"

function Login(){
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        try{
            const response = await axios.post(
                LOGIN_URL, 
                {
                    username: username,
                    password: password,
                },{
                    headers: { 'Request-type': 'login' },
                    withCredentials: true,
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
            // console.error('Error: ', error)
        }
    }

    return(
        <div className="login-div">
            <h1 className="login-title">Welcome again</h1>
            <form className="login-form" onSubmit={handleSubmit}>
                <div className="user-login-div">
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
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required/>
                    </div>
                </div>
                <div className="login-button-div">
                    <button className="login-button" type="submit">Log in</button>
                </div>
            </form>
            <div className="login-footer">
                <p>Don't have an account?</p>
                <Link className="login-link" to={'/signup'}>Signup</Link><br/>
            </div>
        </div>
    )
}

export { Login };