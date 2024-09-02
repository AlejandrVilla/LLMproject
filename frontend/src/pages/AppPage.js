import React, { useState } from 'react';
import axios from 'axios';
import { AutocompleteInput } from '../modules/AutocompleteInput.js';
import { Plan } from "../modules/Plan.js"
import { DefaultAnswer } from '../modules/DefaultAnswer.js';
import { PlanAnswer } from '../modules/PlanAnswer.js';
import { Options } from '../modules/Options.js'
import { ReactComponent as BackSVG } from '../icon/back2.svg'
import { ReactComponent as NextSVG } from '../icon/next.svg'
import BeatLoader from "react-spinners/BeatLoader";
import './App.scss';
import { Link } from 'react-router-dom';

const GET_RECOMENDATION_URL = 'http://127.0.0.1:5006/get-recomendation/';
// const GET_RECOMENDATION_URL = https://www.guideplanner.pro/get-recomendation';
const GET_PLAN_URL = 'http://127.0.0.1:5006/get-plan/';
// const GET_PLAN_URL = 'https://www.guideplanner.pro/get-plan';
let recommendations_tmp;
let planAnswer_tmp;

function App() {
  // loading
  const [loading, setLoading] = useState(false)
  
  // user info
  const [startPoint, setStartPoint] = useState('');
  const [activity, setActivity] = useState('');
  const [recommendations, setRecommendations] = useState('');
  const [planAnswer, setPlanAnswer] = useState('');

  // options values
  const [selectedRadio, setSelectedRadio] = useState('Family');
  const [meters, setMeters] = useState(200);  // Default value
  const [mode, setMode] = useState("DRIVING");

  // hyperparameter
  const temperature = 0.7;
  const radius = meters;
  // const mode = "driving";
  const language = "spanish";

  // When a plan is selected
  const onSelectPlan = (plan) => {
    setLoading(true);
    console.log(plan);
    handleGetPlan(plan);
  }

  const handleGetPlan = async (ind) => {
    planAnswer_tmp = '';
    try{
      const response = await axios.post(
        GET_PLAN_URL,
        {
          ind: ind,
          plan_type: selectedRadio,
          origin: startPoint,
          mode: mode,
          temperature: temperature
        },{
          withCredentials: true,
        }
      );
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
        const response = await axios.post(
          GET_RECOMENDATION_URL, 
          {
            activities: activity,
            origin: startPoint,
            radius: radius,
            language: language,
            temperature: temperature
          },{
            withCredentials: true
          }
        );

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
                onSelect = {onSelectPlan}
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
    <>
      <div className='home-link-div'>
        <Link to={'/'}>Home</Link>
      </div>
      <div className="app">
        <div className="sidebar">
          <h2>Guide Planner</h2>
          <form onSubmit={handleSubmit} className='form'>
            <div>
              <div className="form-group">
                <label htmlFor='start-place'>Start point</label>
                <AutocompleteInput
                  placeholder="Enter a start point"
                  onPlaceChanged={handlePlaceChanged(setStartPoint)}
                />
              </div>
              <div className="form-group">
                <label htmlFor="prompt">Enter your activity</label>
                <textarea
                  value={activity}
                  onChange={(e) => setActivity(e.target.value)}
                  id='prompt'
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
              <button className='search-prompt' type="submit">Search</button>
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
    </>
  );
}

export { App };