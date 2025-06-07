// src/components/PrivateRoute.jsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';

export default function PrivateRoute({ element }) {
  const { isAuthenticated, isLoading } = useAuth0();
  if (isLoading) return <p>Cargando…</p>;
  return isAuthenticated
    ? element
    : <Navigate to="/" replace />;
}