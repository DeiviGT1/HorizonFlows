// src/components/Header.jsx
import React from "react";
import { Link } from "react-router-dom";
import "./Header.css";

export default function Header() {
  return (
    <header className="header">
      {/* Left side: logo + nombre + nav */}
      <div className="flex items-center">
        {/* Logo + texto */}
        <div className="header__branding">
          <svg
            viewBox="0 0 48 48"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M24 4H42V17.3333V30.6667H24V44H6V30.6667V17.3333H24V4Z"
              fill="currentColor"
            />
          </svg>
          <h1>BizMetrics</h1>
        </div>

        {/* Navegación principal */}
        <nav className="header__nav">
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/products">Products</Link>
          <Link to="/customers">Customers</Link>
          <Link to="/companies">Companies</Link>
          <Link to="/invoices">Invoices</Link>
        </nav>
      </div>

      {/* Right side: buscador + notificación + avatar */}
      <div className="header__actions">

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

        {/* Avatar circular */}
        <div
          className="header__avatar"
          style={{
            /* Reemplaza esta URL por la de tu usuario real */
            backgroundImage:
              'url("https://lh3.googleusercontent.com/aida-public/AB6AXuA1VH19HSB_pBdBeUj4XvQILK-KjCccNDKX4j-wSzIgywggdtrWsBPfizX7FqS91HDSaR3lR_gDLC2B1W7UvhO_6YOft6s1ROZ6BscVOuWo_7u02IGM2tMJjjgMIyW1eSJBJNAAsJYfAMKFM2-NDmltkg8JAOnIiwgFUXyCV2r7G4BHSZDrPYsm_6PeHikh42iilV2X8h5No5fMyXHGVQAXLmBufJ1HWXAGcOrN3ry5T5dKdQE12doaM6SpHoELtqv9ZzIBozKDqXpf")',
          }}
        />
      </div>
    </header>
  );
}