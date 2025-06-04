// src/components/Dashboard.jsx
import React from "react";
import "./Dashboard.css";

export default function Dashboard() {
  return (
    <div className="dashboard-root">
      <div className="dashboard-content-container">
        {/* Header: “Dashboard” + subtítulo */}
        <div className="dashboard-header">
          <div className="flex min-w-72 flex-col gap-3">
            <p className="dashboard-header-title">Dashboard</p>
            <p className="dashboard-header-subtitle">Welcome back, Sarah</p>
          </div>
        </div>

        {/* “Key Metrics” título */}
        <h2 className="key-metrics-title">Key Metrics</h2>

        {/* Contenedor de las 3 tarjetas de métricas */}
        <div className="key-metrics-container">
          {/* -------------------- TARJETA 1: Revenue -------------------- */}
          <div className="metric-card">
            <p className="metric-title">Revenue</p>
            <p className="metric-value">$120,000</p>
            <div className="metric-sub-container">
              <p className="metric-sub">This Year</p>
              <p className="metric-trend">+15%</p>
            </div>
            <div className="metric-chart-container">
              {/* Gráfico de línea (SVG) */}
              <svg
                className="chart-line-svg"
                viewBox="-3 0 478 150"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                preserveAspectRatio="none"
              >
                <path
                  d="M0 109C18.1538 109 18.1538 21 36.3077 21C54.4615 21 54.4615 41 72.6154 41C90.7692 41 90.7692 93 108.923 93C127.077 93 127.077 33 145.231 33C163.385 33 163.385 101 181.538 101C199.692 101 199.692 61 217.846 61C236 61 236 45 254.154 45C272.308 45 272.308 121 290.462 121C308.615 121 308.615 149 326.769 149C344.923 149 344.923 1 363.077 1C381.231 1 381.231 81 399.385 81C417.538 81 417.538 129 435.692 129C453.846 129 453.846 25 472 25V149H326.769H0V109Z"
                  fill="url(#paint0_linear_1131_5935)"
                ></path>
                <path
                  d="M0 109C18.1538 109 18.1538 21 36.3077 21C54.4615 21 54.4615 41 72.6154 41C90.7692 41 90.7692 93 108.923 93C127.077 93 127.077 33 145.231 33C163.385 33 163.385 101 181.538 101C199.692 101 199.692 61 217.846 61C236 61 236 45 254.154 45C272.308 45 272.308 121 290.462 121C308.615 121 308.615 149 326.769 149C344.923 149 344.923 1 363.077 1C381.231 1 381.231 81 399.385 81C417.538 81 417.538 129 435.692 129C453.846 129 453.846 25 472 25"
                  stroke="#8dabce"
                  strokeWidth="3"
                  strokeLinecap="round"
                ></path>
                <defs>
                  <linearGradient
                    id="paint0_linear_1131_5935"
                    x1="236"
                    y1="1"
                    x2="236"
                    y2="149"
                    gradientUnits="userSpaceOnUse"
                  >
                    <stop stopColor="#20344b"></stop>
                    <stop offset="1" stopColor="#20344b" stopOpacity="0"></stop>
                  </linearGradient>
                </defs>
              </svg>
              {/* Etiquetas de meses */}
              <div className="chart-labels">
                <p className="chart-label-text">Jan</p>
                <p className="chart-label-text">Feb</p>
                <p className="chart-label-text">Mar</p>
                <p className="chart-label-text">Apr</p>
                <p className="chart-label-text">May</p>
                <p className="chart-label-text">Jun</p>
                <p className="chart-label-text">Jul</p>
              </div>
            </div>
          </div>

          {/* -------------------- TARJETA 2: Expenses -------------------- */}
          <div className="metric-card">
            <p className="metric-title">Expenses</p>
            <p className="metric-value">$80,000</p>
            <div className="metric-sub-container">
              <p className="metric-sub">This Year</p>
              <p className="metric-trend">+10%</p>
            </div>
            <div className="chart-bar-grid">
              {/* Cada div.chart-bar tiene un style inline con la altura deseada */}
              <div
                className="chart-bar"
                style={{ height: "70%" }}
              ></div>
              <p className="chart-bar-label">Jan</p>
              <div
                className="chart-bar"
                style={{ height: "20%" }}
              ></div>
              <p className="chart-bar-label">Feb</p>
              <div
                className="chart-bar"
                style={{ height: "60%" }}
              ></div>
              <p className="chart-bar-label">Mar</p>
              <div
                className="chart-bar"
                style={{ height: "70%" }}
              ></div>
              <p className="chart-bar-label">Apr</p>
              <div
                className="chart-bar"
                style={{ height: "30%" }}
              ></div>
              <p className="chart-bar-label">May</p>
              <div
                className="chart-bar"
                style={{ height: "20%" }}
              ></div>
              <p className="chart-bar-label">Jun</p>
              <div
                className="chart-bar"
                style={{ height: "60%" }}
              ></div>
              <p className="chart-bar-label">Jul</p>
            </div>
          </div>

          {/* -------------------- TARJETA 3: Profit -------------------- */}
          <div className="metric-card">
            <p className="metric-title">Profit</p>
            <p className="metric-value">$40,000</p>
            <div className="metric-sub-container">
              <p className="metric-sub">This Year</p>
              <p className="metric-trend">+20%</p>
            </div>
            <div className="chart-horizontal-grid">
              {/* Cada par <label + barra> ocupa una fila */}
              <p className="chart-bar-label">Jan</p>
              <div className="chart-horizontal-bar-wrapper">
                <div
                  className="chart-horizontal-bar"
                  style={{ width: "60%" }}
                ></div>
              </div>
              <p className="chart-bar-label">Feb</p>
              <div className="chart-horizontal-bar-wrapper">
                <div
                  className="chart-horizontal-bar"
                  style={{ width: "20%" }}
                ></div>
              </div>
              <p className="chart-bar-label">Mar</p>
              <div className="chart-horizontal-bar-wrapper">
                <div
                  className="chart-horizontal-bar"
                  style={{ width: "60%" }}
                ></div>
              </div>
              <p className="chart-bar-label">Apr</p>
              <div className="chart-horizontal-bar-wrapper">
                <div
                  className="chart-horizontal-bar"
                  style={{ width: "70%" }}
                ></div>
              </div>
              <p className="chart-bar-label">May</p>
              <div className="chart-horizontal-bar-wrapper">
                <div
                  className="chart-horizontal-bar"
                  style={{ width: "80%" }}
                ></div>
              </div>
              <p className="chart-bar-label">Jun</p>
              <div className="chart-horizontal-bar-wrapper">
                <div
                  className="chart-horizontal-bar"
                  style={{ width: "20%" }}
                ></div>
              </div>
              <p className="chart-bar-label">Jul</p>
              <div className="chart-horizontal-bar-wrapper">
                <div
                  className="chart-horizontal-bar"
                  style={{ width: "30%" }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Sección “Summary” (Total Revenue, Total Expenses, …) */}
        <h2 className="summary-title">Summary</h2>
        <div className="summary-grid">
          <div className="summary-item">
            <p className="summary-item-title">Total Revenue</p>
            <p className="summary-item-value">$120,000</p>
          </div>
          <div className="summary-item">
            <p className="summary-item-title">Total Expenses</p>
            <p className="summary-item-value">$80,000</p>
          </div>
          <div className="summary-item">
            <p className="summary-item-title">Net Profit</p>
            <p className="summary-item-value">$40,000</p>
          </div>
          <div className="summary-item">
            <p className="summary-item-title">Outstanding Invoices</p>
            <p className="summary-item-value">5</p>
          </div>
          <div className="summary-item">
            <p className="summary-item-title">Overdue Invoices</p>
            <p className="summary-item-value">2</p>
          </div>
          <div className="summary-item">
            <p className="summary-item-title">Total Contacts</p>
            <p className="summary-item-value">100</p>
          </div>
        </div>
      </div>
    </div>
  );
}