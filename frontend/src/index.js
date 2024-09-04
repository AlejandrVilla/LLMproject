import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { LoadScript } from '@react-google-maps/api';

import { App } from './pages/AppPage';
import { Home } from './pages/HomePage'
import { Login } from './pages/LoginPage';
import { Signup } from './pages/SignUpPage';

import './index.scss';

const libraries = ['places'];
const apiKey  = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home/>,
    errorElement: <p>404 not found</p>
  },
  {
    path: '/app',
    element: <App/>
  },
  {
    path: '/login',
    element: <Login/>
  },
  {
    path: '/signup',
    element: <Signup/>
  }
])

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <LoadScript googleMapsApiKey={apiKey} libraries={libraries}>
      <RouterProvider router={router}/>
    </LoadScript>
  </React.StrictMode>
);