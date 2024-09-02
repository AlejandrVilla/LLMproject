import React, { useState } from 'react';
import './Options.scss'

const Options = ({ selectedRadio, onRadioChanged, selectedMeter, onMeterChanged, selectMode, onModeChanged }) => {
    const [selectedOption, setSelectedOption] = useState(selectedRadio);
    const [meters, setMeters] = useState(selectedMeter);  // Default value
    const [mode, setMode] = useState(selectMode);

    // When type of plan is selected
    const handleRadioChange = (e) => {
        setSelectedOption(e.target.value);
        onRadioChanged(e.target.value)
    };

    // when scroll bar for meters change
    const handleMetersChange = (e) => {
        setMeters(e.target.value);
        onMeterChanged(e.target.value);
    };
    
    // when mode is changed
    const handleModeChange = (e) => {
        setMode(e.target.value);
        onModeChanged(e.target.value)
    }

    return (
        <>
            <div className='meters'>
                <label htmlFor='meter-range'>Radio in meters</label>
                <input
                    className='meter-range'
                    type="range"
                    min="100"
                    max="500"
                    value={meters}
                    onChange={handleMetersChange}
                    id='meter-range'
                /> {meters}
            </div>
            <div className='mode-div'>
                <p>Mode</p>
                <div className='mode-radio-div'>
                    <div>
                        <label className="form-control">
                            <input
                                type="radio"
                                name="mode"
                                value="DRIVING"
                                checked={mode === "DRIVING"}
                                onChange={handleModeChange}
                            />
                            <div className="check"></div>
                            Driving
                        </label>
                    </div>
                    <div>
                        <label className="form-control">
                            <input
                                type="radio"
                                name="mode"
                                value="WALKING"
                                checked={mode === "WALKING"}
                                onChange={handleModeChange}
                            />
                            <div className="check"></div>
                            walking
                        </label>
                    </div>
                </div>
            </div>
            <div className='type-plan-div'>
                <p>Plan</p>
                <div className='plan-radio-div'>
                    <div>
                        <label className="form-control">
                            <input
                                type="radio"
                                name="option"
                                value="Family"
                                checked={selectedOption === 'Family'}
                                onChange={handleRadioChange}
                            />
                            <div className="check"></div>
                            Family
                        </label>
                    </div>
                    <div>
                        <label className="form-control">
                            <input
                                type="radio"
                                name="option"
                                value="Romantic"
                                checked={selectedOption === 'Romantic'}
                                onChange={handleRadioChange}
                            />
                            <div className="check"></div>
                            Romantic
                        </label>
                    </div>
                    <div>
                        <label className="form-control">
                            <input
                                type="radio"
                                name="option"
                                value="Tourism"
                                checked={selectedOption === 'Tourism'}
                                onChange={handleRadioChange}
                            />
                            <div className="check"></div>
                            Tourism
                        </label>
                    </div>
                </div>
            </div>
        </>
    );
};

export { Options };