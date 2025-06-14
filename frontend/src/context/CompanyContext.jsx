import React, { createContext, useContext, useEffect, useState } from 'react';
import { useApi } from '../hooks/useApi';
import { useAuth0 } from '@auth0/auth0-react';

const CompanyContext = createContext(null);

export const useCompany = () => useContext(CompanyContext);

export const CompanyProvider = ({ children }) => {
  const [currentCompany, setCurrentCompany] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const api = useApi();
  
  // Obtenemos tanto el estado de autenticación como el estado de carga de Auth0
  const { isAuthenticated, isLoading: isAuthLoading } = useAuth0();

  useEffect(() => {
    // 1. No hacemos nada hasta que Auth0 haya terminado de cargar.
    if (isAuthLoading) {
      return; // Salimos del efecto si Auth0 todavía está en proceso.
    }

    const fetchCompany = async () => {
      // 2. Si el usuario está autenticado, intentamos obtener los datos de la compañía.
      if (isAuthenticated) {
        try {
          const response = await api.get('/business/current');
          setCurrentCompany(response.data);
        } catch (error) {
          console.error("Fallo al obtener el contexto de la compañía:", error);
          // Aquí podrías establecer un estado de error si lo deseas.
        }
      }
      
      // 3. Ya sea que el usuario esté autenticado, no lo esté, o haya habido un error,
      // el proceso de carga ha terminado.
      setIsLoading(false);
    };

    fetchCompany();
  }, [api, isAuthenticated, isAuthLoading]); // El efecto se vuelve a ejecutar si estos valores cambian.

  // Mostramos un indicador de carga mientras Auth0 carga O mientras buscamos la compañía.
  if (isLoading) { 
    return <p className="text-white text-center p-10">Cargando Datos de Usuario y Compañía...</p>;
  }

  // Si hemos terminado de cargar, renderizamos la aplicación.
  return (
    <CompanyContext.Provider value={{ currentCompany }}>
      {children}
    </CompanyContext.Provider>
  );
};
