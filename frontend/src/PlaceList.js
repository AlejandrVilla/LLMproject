import React from "react";
import {PlaceItem} from "./PlaceItem";
import "./PlaceList.css";

// Component for a list of places
const PlaceList = ({places, data_key, onSelect}) => {
    // When a plan is selected
    const onSelectPlan = (e) => {
        // console.log(data_key + 1)
        onSelect(data_key);
    }

    return(
        <div className="placelist-div">
            <div className="placelist-title">
                {/* <p>Plan {data_key+1}</p> */}
                <p className="title" onClick={onSelectPlan}>choose plan {data_key+1}</p>
            </div>
            {places.map(place => (    
                <PlaceItem 
                    key={place.place_id}
                    place={place}
                />
            ))}
        </div>
    )
}

export {PlaceList}