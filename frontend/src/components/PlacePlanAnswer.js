import React from "react";
import './PlacePlanAnswer.scss'

// Component for a final plan
function PlacePlanAnswer({place}){
    // console.log(place)
    return (
        <div className="place-answer-div">
            <p className="place-answer-name">{place.name}</p>
            <a href={place.maps_url} target="_blank" rel="noreferrer noopener">Maps link</a>
            {/* {place.opened ?(
                <p className="place-answer-opened">It's opened now!</p>
            ) : (
                <p className="place-answer-opened">It's not opened now</p>
            )} */}
            { place.phone_number ? (
                <p className="place-answer-phone">Contact: {place.phone_number}</p>
            ) : (
                <p className="place-answer-phone">No phone number</p>
            )
            }
            <p>duration: {place.duration}</p>
        </div>
    )
}

export {PlacePlanAnswer};