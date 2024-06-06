import React, { useState } from 'react';
import axios from 'axios';
import { LoadScript } from '@react-google-maps/api';
import AutocompleteInput from './AutocompleteInput.js';
import './App.css';

const libraries = ['places'];
const apiKey  = "AIzaSyCSRyW3hVI6HV-6xgkwqgSJMPWgMKELvYk"

function App() {
  const [referencePlace, setReferencePlace] = useState('');
  const [startPoint, setStartPoint] = useState('');
  const [activity, setActivity] = useState('');
  const [recommendations, setRecommendations] = useState('');
  const temperature = 0.7;
  const radius = 100;
  const order_by = "rating";
  const mode = "driving";
  const language = "spanish"

  const handlePlaceChanged = (placeSetter) => (place) => {
    placeSetter(place);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
        const response = await axios.post('https://www.guideplanner.pro/get-recomendation', {
            reference_place: referencePlace, 
            order_by: order_by,
            origin: startPoint,
            activities: activity,
            radius: radius,
            mode: mode,
            language: language,
            temperature: temperature
        });

        const data = response.data;
        setRecommendations(data.content);
    } catch (error) {
        console.error('Error fetching recommendations:', error);
    }
  };

  return (
    <LoadScript googleMapsApiKey={apiKey} libraries={libraries}>
      <div className="app">
        <div className="sidebar">
          <h2>Guide Planner</h2>
          <form onSubmit={handleSubmit} className='form'>
            <div className="form-group">
              <label>Reference place</label>
              <AutocompleteInput
                placeholder="Enter a reference place"
                onPlaceChanged={handlePlaceChanged(setReferencePlace)}
              />
            </div>
            <div className="form-group">
              <label>Start point</label>
              <AutocompleteInput
                placeholder="Enter a start point"
                onPlaceChanged={handlePlaceChanged(setStartPoint)}
              />
            </div>
            <div className="form-group">
              <label>Enter your activity</label>
              <textarea
                value={activity}
                onChange={(e) => setActivity(e.target.value)}
                required
              ></textarea>
            </div>
            <div className='div_button'>
              <button type="submit">Search</button>
            </div>
          </form>
        </div>
          <div className='answer'>
            <div className='model_answer'>
              <h1>Plan for your activity</h1>
              {recommendations ? (
                <div className="results">
                  <p>{recommendations}</p>
                </div>
              ) : (
                <div className="results">
                  <p style={{"textAlign": "center"}}>
                    This application provides personalized activity recommendations based on your input.
                  </p>
                  <ol>
                    <li>
                      Enter a reference place.
                    </li><p></p>
                    <li>
                      Enter a starting point.
                    </li><p></p>
                    <li>
                      Add the plan you want to do
                    </li>
                  </ol>
                </div>
              )}
            </div>
          </div>
      </div>
    </LoadScript>
  );
}

export default App;