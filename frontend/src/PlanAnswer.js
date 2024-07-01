import { useState } from 'react'
import { Link, BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './PlanAnswer.css'
import { PlacePlanAnswer } from "./PlacePlanAnswer";
import {
    Box,
    Flex,
  } from '@chakra-ui/react'
import {
    GoogleMap,
    Marker,
    DirectionsRenderer,
} from '@react-google-maps/api'

// Component to render an answer
function PlanAnswer({answer, startPoint}){
    console.log(answer.places_info);
    return(
        <Router>
            <Routes>
                <Route path="/" element={<Answer answer={answer} startPoint={startPoint} />} />
                <Route path="/map" element={<Map answer={answer} startPoint={startPoint} />} />
            </Routes>
        </Router>
    )
}

// Final answer
function Answer({answer, startPoint}){
    return (
        <div className="plan-answer-div">
            <h1>Plan for your activity</h1>
            <Link className='map-link' to="/map">
                <h3>Show plan in map</h3>
            </Link>
            <p className="plan-answer">
                {answer.content}
            </p>
            <div className="places-info-div">
                {answer.places_info.map(place => (
                    <PlacePlanAnswer 
                        key = {place.place_id}
                        place = {place}
                    />
                ))}
            </div>
        </div>
    )
}

// Component to show a map
function Map({answer, startPoint}){
    const [directionsResponse, setDirectionsResponse] = useState(null)
    const [distance, setDistance] = useState('')
    const [duration, setDuration] = useState('')
    
    let start = startPoint
    let center = answer.places_info[0].location
    let end = answer.places_info[answer.places_info.length-1].location
    let total_time = 0;
    let mode = answer.places_info[0].mode
    
    // Stop points in a route
    async function calculateRoute() {
        let waypts = [];
        // extract wait points
        answer.places_info.map(place => {
            total_time += parseInt(place.duration.split(' ')[0])
            waypts.push(
                {
                    "location": place.location,
                    "stopover": true
                }
            );
        });

        const directionsService = new google.maps.DirectionsService()
        const results = await directionsService.route({
            origin: start,
            destination: end,
            waypoints: waypts,
            travelMode: mode,
            // optimizeWaypoints: true,
            // eslint-disable-next-line no-undef
            travelMode: google.maps.TravelMode.DRIVING,
        })
        setDirectionsResponse(results)
        setDistance(results.routes[0].legs[0].distance.text)
        setDuration(total_time)
    }
    // console.log(directionsResponse);
    if(!directionsResponse){
        calculateRoute();
    }
    return (
        <div className='plan-map-div'>
            <Link className='return-link' to="/">
                <h3>Return to plan</h3>
            </Link>
            <p>{duration} min by {answer.places_info[0].mode}</p>
            <Flex
                position='relative'
                flexDirection='column'
                alignItems='center'
                h='auto'
                w='auto'
            >
                <Box position='relative' left={0} top={0} h='400px' w='550px'>
                    {/* Google Map Box */}
                    <GoogleMap
                        center={center}
                        zoom={15}
                        mapContainerStyle={{ width: '100%', height: '100%' }}
                        options={{
                            // zoomControl: false,
                            kustreetViewControl: false,
                            mapTypeControl: false,
                            // fullscreenControl: false,
                        }}
                    >
                    <Marker position={center} />
                    {directionsResponse && (
                        <DirectionsRenderer directions={directionsResponse} />
                    )}
                    </GoogleMap>
                </Box>
            </Flex>
        </div>
    )
}

export {PlanAnswer};