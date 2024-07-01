import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LoadScript } from '@react-google-maps/api';
import { AutocompleteInput } from './AutocompleteInput.js';
import { Plan } from "./Plan.js"
import { DefaultAnswer } from './DefaultAnswer.js';
import { PlanAnswer } from './PlanAnswer.js';
import { Options } from './Options.js'
import { ReactComponent as BackSVG } from './icon/back2.svg'
import { ReactComponent as NextSVG } from './icon/next.svg'
import BeatLoader from "react-spinners/BeatLoader";
import './App.css';

const libraries = ['places'];
const apiKey  = "AIzaSyCSRyW3hVI6HV-6xgkwqgSJMPWgMKELvYk"
let recommendations_tmp;
let planAnswer_tmp;

function App() {
  // loading
  const [loading, setLoading] = useState(false)
  
  // plan values
  const [selectPlan, setSelectPlan] = useState(null);
  
  // user info
  const [startPoint, setStartPoint] = useState('');
  const [activity, setActivity] = useState('');
  const [recommendations, setRecommendations] = useState('');
  const [planAnswer, setPlanAnswer] = useState('');

  // options values
  const [selectedRadio, setSelectedRadio] = useState('Family');
  const [meters, setMeters] = useState(200);  // Default value
  const [mode, setMode] = useState("driving");

  // hyperparameter
  const temperature = 0.7;
  const radius = meters;
  // const mode = "driving";
  const language = "spanish";

  // selectPlan, setSelectPlan
  const onSelectPlan = (planSetter) => (plan) => {
    setLoading(true);
    planSetter(plan);
  }

  // useEffect to log selectedOption whenever it changes
  useEffect(() => {
    if(selectPlan != null){
      console.log(selectPlan+1);
      handleGetPlan();
    }
  }, [selectPlan]);

  // console.log(startPoint)
  const handleGetPlan = async () => {
    planAnswer_tmp = '';
    try{
      const response = await axios.post('https://www.guideplanner.pro/get-plan',{
      // const response = await axios.post('http://127.0.0.1:5005/get-plan',{
        ind: selectPlan,
        plan_type: selectedRadio,
        origin: startPoint,
        mode: mode,
        temperature: temperature
      });
      const data = response.data;
      // console.log(data);  
      setPlanAnswer(data);
      recommendations_tmp = recommendations
      setRecommendations('');
      setLoading(false);
    }catch (error){
      console.error('Error fetching plan:', error);
    }
  }

  // startPoint, setStartPoint
  const handlePlaceChanged = (placeSetter) => (place) => {
    placeSetter(place);
  };

  // selectedRadio, setSelectedRadio
  const handleRadioChanged = (radioSetter) => (radio) => {
    radioSetter(radio);
  };
  // console.log(selectedRadio);
  
  // meters, setMeters
  const handleMetersChanged = (meterSetter) => (meter) => {
    meterSetter(meter);
  }
  // console.log(meters);

  const handleModeChange = (modeSetter) => (mode) => {
    modeSetter(mode)
  }

  // post to get-recomendation ms
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
        const response = await axios.post('https://www.guideplanner.pro/get-recomendation', {
        // const response = await axios.post('http://127.0.0.1:5001/get-recomendation', {
            activities: activity,
            origin: startPoint,
            radius: radius,
            language: language,
            temperature: temperature
        });

        const data = response.data;
        // console.log(data);
        setRecommendations(data.content);
        setLoading(false);
    } catch (error) {
        console.error('Error fetching recommendations:', error);
    }
  };

  // Component for plan
  let final_plan;
  if (recommendations){
    final_plan = <Plan 
                recommendations = {recommendations}
                onSelect = {onSelectPlan(setSelectPlan)}
              />
  }
  else if(planAnswer)
  {
    final_plan = <PlanAnswer answer={planAnswer} startPoint={startPoint} />
  }
  else{
    final_plan = <DefaultAnswer/>
  }

  // Back button
  const handleBack = () => {
    if(recommendations_tmp){
      setRecommendations(recommendations_tmp);
      planAnswer_tmp = planAnswer;
      // console.log(planAnswer_tmp);
      setPlanAnswer('');
      recommendations_tmp = ''
    }
  };
  let back_icon;
  if (recommendations_tmp){
    back_icon = <BackSVG 
                    className="Icon-svg"
                  />
  }

  // Next button
  const handleNext = () => {
    if(planAnswer_tmp){
      recommendations_tmp = recommendations;
      setRecommendations('');
      // console.log(recommendations_tmp);
      setPlanAnswer(planAnswer_tmp);
      planAnswer_tmp = '';
    }
  };
  let next_icon;
  if(planAnswer_tmp){
    next_icon = <NextSVG
                    className="Icon-svg"
                />
  }

  // Component
  return (
    <LoadScript googleMapsApiKey={apiKey} libraries={libraries}>
      <div className="app">
        <div className="sidebar">
          <h2>Guide Planner</h2>
          <form onSubmit={handleSubmit} className='form'>
            <div>
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
            </div>
            <div className='options-div'>
              <Options
                selectedRadio = {selectedRadio}
                onRadioChanged = {handleRadioChanged(setSelectedRadio)}
                selectedMeter = {meters}
                onMeterChanged = {handleMetersChanged(setMeters)}
                selectMode = {mode}
                onModeChanged = {handleModeChange(setMode)}
              />
            </div>
            <div className='div_button'>
              <button type="submit">Search</button>
            </div>
          </form>
        </div>
          <div className='answer'>
            <div className='model_answer'>
              {loading?(
                <div className='loading-div'>
                  <p>wait a moment</p>
                  <BeatLoader color='#d63736' loading={loading}/>
                </div>
                ):(
                <div className="results">
                  <div className='icon-div'>
                    <div 
                      className='Back-icon-div'
                      onClick={handleBack}
                    >
                      {back_icon}
                    </div>
                    <div className='Next-icon-div'
                      onClick={handleNext}
                    >
                      {next_icon}
                    </div>
                  </div>
                    {final_plan}
                </div>
              )}
            </div>
          </div>
      </div>
    </LoadScript>
  );
}

export default App;