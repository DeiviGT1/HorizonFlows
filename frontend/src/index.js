// frontend/src/index.js

import React from 'react';
import ReactDOM from 'react-dom/client';

// No importamos NADA más. Ni App.js, ni Auth0, ni CSS.

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <div style={{ 
      padding: '50px', 
      textAlign: 'center', 
      color: 'white', 
      fontSize: '32px', 
      fontFamily: 'sans-serif' 
    }}>
      Hola Mundo de Prueba
    </div>
  </React.StrictMode>
);