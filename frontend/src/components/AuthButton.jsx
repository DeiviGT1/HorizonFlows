// src/components/AuthButton.jsx
import React from "react";
import { useAuth0 } from "@auth0/auth0-react";

export default function AuthButton() {
  const { isAuthenticated, isLoading, loginWithRedirect, logout } = useAuth0();

  if (isLoading) {
    // Puedes mostrar un skeleton o simplemente nada
    return <button className="animate-pulse" disabled>Cargando…</button>;
  }

  return isAuthenticated ? (
    <button
      onClick={() =>
        logout({ logoutParams: { returnTo: window.location.origin } })
      }
    >
      Cerrar sesión
    </button>
  ) : (
    <button onClick={() => loginWithRedirect()}>Iniciar sesión</button>
  );
}