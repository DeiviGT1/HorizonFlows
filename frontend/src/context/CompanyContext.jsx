// frontend/src/context/CompanyContext.jsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import { useApi } from '../hooks/useApi';
import { useAuth0 } from '@auth0/auth0-react';

const CompanyContext = createContext(null);

export const useCompany = () => useContext(CompanyContext);

export const CompanyProvider = ({ children }) => {
  const [currentCompany, setCurrentCompany] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const api = useApi();
  const { isAuthenticated } = useAuth0();

  useEffect(() => {
    const fetchCompany = async () => {
      if (!isAuthenticated) return;
      try {
        // This endpoint will be created in the next step
        const response = await api.get('/business/current');
        setCurrentCompany(response.data);
      } catch (error) {
        console.error("Failed to fetch company context", error);
        // Handle error, e.g., redirect to a "company not found" page
      } finally {
        setIsLoading(false);
      }
    };

    fetchCompany();
  }, [api, isAuthenticated]);

  if (isLoading) {
    return <p className="text-white text-center p-10">Loading Company Data...</p>;
  }

  return (
    <CompanyContext.Provider value={{ currentCompany }}>
      {children}
    </CompanyContext.Provider>
  );
};