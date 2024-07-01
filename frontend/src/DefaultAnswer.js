import React from "react";

// Component for default answer
function DefaultAnswer(){
    return(
        <>
            <h1>Plans for your activity</h1>
            <p style={{"textAlign": "center"}}>
            This application provides personalized activity recommendations based on your preferences.
            </p>
            <ol>
            <li>
                Enter a starting point.
            </li><p></p>
            <li>
                Add the plan you want to do
            </li><p></p>
            <li>
                Personalized your plan options
            </li>
            </ol>
        </>
    )
}

export {DefaultAnswer};