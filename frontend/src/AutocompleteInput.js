import React, { useState, useRef } from 'react';
import { Autocomplete } from '@react-google-maps/api';

const AutocompleteInput = ({ placeholder, onPlaceChanged }) => {
  const [autocomplete, setAutocomplete] = useState(null);
  const inputRef = useRef(null);

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
        ref={inputRef}
        type="text"
        placeholder={placeholder}
        required
      />
    </Autocomplete>
  );
};

export default AutocompleteInput;