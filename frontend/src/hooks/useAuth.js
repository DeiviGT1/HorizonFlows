// src/hooks/useAuth.js
import { useAuth0 } from "@auth0/auth0-react";

export function useAuth() {
  const {
    isAuthenticated,
    isLoading,
    user,
    loginWithRedirect,
    logout,
    getAccessTokenSilently,
  } = useAuth0();

  /**
   * Obtiene el token de acceso o lanza un error si no hay sesión.
   */
  async function getToken() {
    if (!isAuthenticated) {
      throw new Error("No autenticado");
    }
    return getAccessTokenSilently({
      audience: process.env.REACT_APP_API_AUDIENCE,
    });
  }

  return {
    isAuthenticated,
    isLoading,
    user,
    login: loginWithRedirect,
    logout: () => logout({ returnTo: window.location.origin }),
    getToken,
  };
}