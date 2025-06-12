// frontend/src/components/AdminRoute.jsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';

export default function AdminRoute({ element }) {
  const { user, isAuthenticated, isLoading } = useAuth0();

  console.log("user",user);
  console.log("isAuthenticated",isAuthenticated);
  console.log("isLoading",isLoading);

  // 1. Mientras carga la sesión, no mostrar nada para evitar parpadeos
  if (isLoading) {
    return <p className="text-white text-center p-10">Verificando sesión...</p>;
  }

  // 2. Definimos el namespace que usaste en la Action de Auth0
  const adminRoleNamespace = 'https://horizonflows.com/roles';
  console.log("adminRoleNamespace",adminRoleNamespace);

  // 3. Verificamos si el usuario está autenticado Y si tiene el rol de 'admin'
  const isUserAdmin = 
    isAuthenticated &&
    user &&
    user[adminRoleNamespace]?.includes('admin');

  // 4. Si es admin, muestra la página. Si no, lo redirige a la raíz.
  return isUserAdmin ? element : <Navigate to="/" replace />;
}