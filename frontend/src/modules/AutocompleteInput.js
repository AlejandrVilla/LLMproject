import React, { useState, useRef } from 'react';
import { Autocomplete } from '@react-google-maps/api';

// Autocomplete component
const AutocompleteInput = ({ placeholder, onPlaceChanged }) => {
  const [autocomplete, setAutocomplete] = useState(null);
  const inputRef = useRef(null);

  // Load placeholder
  const onLoad = (autocompleteInstance) => {
    setAutocomplete(autocompleteInstance);
  };

  const onPlaceChangedHandler = () => {
    if (autocomplete !== null) {
      const place = autocomplete.getPlace();
      console.log(place.formatted_address)
      onPlaceChanged(place.formatted_address);
    } else {
      console.log('Autocomplete is not loaded yet!');
    }
  };

  return (
    <Autocomplete
      onLoad={onLoad}
      onPlaceChanged={onPlaceChangedHandler}
    >
      <input
        className='autocomplete-input'
        ref={inputRef}
        type="text"
        placeholder={placeholder}
        id='start-place'
        required
      />
    </Autocomplete>
  );
};

export {AutocompleteInput};