// src/index.js
import React from "react";
import ReactDOM from "react-dom/client"; // 👈 Notice the change here
import App from "./App";
import { Auth0Provider } from "@auth0/auth0-react";
import "./index.css";

const domain = process.env.REACT_APP_AUTH0_DOMAIN;
const clientId = process.env.REACT_APP_AUTH0_CLIENT_ID;
const audience = process.env.REACT_APP_AUTH0_AUDIENCE;
const redirectUri = window.location.origin;

const root = ReactDOM.createRoot(document.getElementById("root")); // 👈 createRoot instead of render
root.render(
  <React.StrictMode>
    <Auth0Provider
      domain={domain}
      clientId={clientId}
      cacheLocation="localstorage"   // ⬅️  NUEVO
      useRefreshTokens={true}  
      authorizationParams={{
        redirect_uri: redirectUri,
        audience,
        scope: "openid profile email",
      }}  
    >

      <App />
    </Auth0Provider>
  </React.StrictMode>
);
