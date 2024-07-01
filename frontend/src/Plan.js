import React from 'react';
import {PlaceList} from "./PlaceList"
import "./Plan.css"

// Component to show plans
function Plan({recommendations, onSelect}){
    // console.log(recommendations);
    let index = 0;
    return(
        <div className='plan-div'>
            <h2>Select your plan</h2>
            {recommendations.map(places => (
                <PlaceList
                    key={index}
                    data_key={index++}
                    places={places} 
                    onSelect={onSelect}
                />
            ))}
        </div>
    )
}

export {Plan};