// src/components/Header.jsx
import React from "react";
import { Link } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import AuthButton from "./AuthButton";
import "./Header.css";

export default function Header() {
  const { isAuthenticated, isLoading, user } = useAuth0();

  // Opcional: mientras Auth0 hidrata la sesión evita el parpadeo
  if (isLoading) return null;

  const adminRoleNamespace = 'https://horizonflows.com/roles';
  const isUserAdmin = user && user[adminRoleNamespace]?.includes('admin');


  return (
    <header className="header flex items-center justify-between">
      {/* Branding + navegación */}
      <div className="flex items-center gap-8">
        <div className="header__branding flex items-center gap-2">
          <svg /* …logo… */ />
          <h1>BizMetrics</h1>
        </div>

        {/* Menú solo para usuarios autenticados */}
        {isAuthenticated && (
          <nav className="header__nav flex gap-4">
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/products">Products</Link>
            <Link to="/customers">Customers</Link>
            <Link to="/companies">Companies</Link>
            <Link to="/invoices">Invoices</Link>
            {isUserAdmin && (
              <Link to="/admin/onboarding" style={{ color: '#21A0A0' }}>Admin Onboarding</Link>
            )}
          </nav>
        )}
      </div>

      {/* Acciones */}
      <div className="header__actions flex items-center gap-4">
        <AuthButton />

        {isAuthenticated && (
          <>
                    {/* Botón de notificación (campana) */}
        <button className="header__icon-button">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            viewBox="0 0 256 256"
          >
            <path d="M221.8,175.94C216.25,166.38,208,139.33,208,104a80,80,0,1,0-160,0c0,35.34-8.26,62.38-13.81,71.94A16,16,0,0,0,48,200H88.81a40,40,0,0,0,78.38,0H208a16,16,0,0,0,13.8-24.06ZM128,216a24,24,0,0,1-22.62-16h45.24A24,24,0,0,1,128,216ZM48,184c7.7-13.24,16-43.92,16-80a64,64,0,1,1,128,0c0,36.05,8.28,66.73,16,80Z" />
          </svg>
        </button>


            {/* Avatar del usuario */}
            <div
              className="header__avatar"
              style={{
                backgroundImage: `url("${user?.picture ?? ""}")`,
              }}
            />
          </>
        )}
      </div>
    </header>
  );
}