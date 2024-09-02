import axios from "axios";
import React, {useEffect, useState} from "react";
import { Link } from "react-router-dom";
import { PlaceSearched } from "../components/PlaceSearched";
import { PromptsSearched } from "../components/PromptsSearched";
import './home.scss'

const USER_URL = "http://127.0.0.1:5006/@me/"
const LOGOUT_URL = "http://127.0.0.1:5006/logout/"

function Home(){
    const [uid, setUid] = useState("")
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("");
    const [name, setName] = useState("");
    const [lastName, setLastName] = useState("");
    const [prompts, setPrompts] = useState();
    const [places, setPlaces] = useState();

    const logoutUser = async () => {
        try{
            const response = await axios.post(
                LOGOUT_URL, 
                {},
                {
                    headers: { 'Request-type': 'logout' },
                    withCredentials: true
                }
            );
            alert('succesfully logout')
        }catch (error){
            console.error('error trying to logout')
        }
        window.location.href = "/";
    };

    useEffect(() => {
        (async () => {
            try {
                const response = await axios.get(
                    USER_URL, 
                    {
                        headers: { 'Request-type': '@me' },
                        withCredentials: true
                    }
                );
                const data = response.data
                setUid(data.uid)
                setUsername(data.username)
                setEmail(data.email)
                setName(data.name)
                setLastName(data.last_name)
                setPrompts(data.prompts);
                setPlaces(data.places);
            }catch (error){
                console.error('Not logged: ', error)
            }
        })();
    }, []);
    return(
        <div className="home">
            {uid?(
                <div className="info-home">
                    <div className="user-card">
                        <h1>Your personal info</h1>
                        <div className="user-info">
                            <div>
                                <p className="label">username</p>
                                <p className="label-value">{username}</p>
                            </div>
                            <div>
                                <p className="label">email</p>
                                <p className="label-value">{email}</p>
                            </div>
                            <div>
                                <p className="label">Name</p>
                                <p className="label-value">{name}</p>
                            </div>
                            <div>
                                <p className="label">Last name</p>
                                <p className="label-value">{lastName}</p>
                            </div>
                        </div>
                        <button className="logout-button" onClick={logoutUser}>Log out</button>
                    </div>
                    <div className="user-app-info-div">
                        <div className="app-info-div">
                            <div className="questions-div">
                                <h2 className="user-app-title">Your last searches</h2>
                                <div className="user-app-content">
                                    {
                                        prompts.map((prompt) => (
                                            <PromptsSearched
                                                key={prompt[0]}
                                                prompt={prompt[1]}
                                            />
                                        ))
                                    }
                                </div>
                            </div>
                            <div className="places-div">
                                <h2 className="user-app-title">Last places</h2>
                                <div className="user-app-content">
                                    {
                                        places.map((place) => (
                                            <PlaceSearched 
                                                key={place[0]}
                                                place={place[1]}
                                            />
                                        ))
                                    }
                                </div>
                            </div>
                        </div>
                        <Link className="app-button" to={'/app'}>
                            <p>Go to app</p></Link>
                    </div>
                </div>
            ):(
                <div className="home-links">
                    <Link to={'/login'}>Login</Link>
                    <Link to={'/signup'}>Sign up</Link>
                </div>
            )}
        </div>
    )
}

export { Home };