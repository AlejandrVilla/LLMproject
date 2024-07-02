import React from "react";
import "./PlaceItem.css"

// Component for a place
function PlaceItem({place}){
    // console.log(place)
    return(
        <div className="place-div">
            <p className="place-type">{place.type}</p>
            <div className="place-div-info">
                <p className="place-name">{place.name}</p>
                {place.phone_number ? (<p className="place-number">{place.phone_number}</p>) : <p>No number</p>}
                {place.rating ? (<p className="place-rating">rating: {place.rating}</p>) : <p>No rating</p> }
                {place.maps_url ? (<a href={place.maps_url} target="_blank" rel="noreferrer noopener"><p>Maps link</p></a>) : <p>No maps link</p> }
            </div>
        </div>
    )
}

export {PlaceItem};