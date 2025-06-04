// src/pages/Invoices.jsx
import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/axios";
// Si decides sacar el CSS a un archivo aparte, basta con:
// import "./Invoices.css";

export default function Invoices() {
  const qc = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    company_id: "",
    customer_id: "",
    lines: [{ product_id: "", qty: "" }],
  });

  // 1️⃣ Traer lista de facturas
  const { data: invoices, isLoading, error } = useQuery({
    queryKey: ["invoices"],
    queryFn: async () => {
      const res = await api.get("/invoices/");
      return res.data;
    },
  });

  // 2️⃣ Mutación: crear factura
  const createMutation = useMutation({
    mutationFn: async (newInv) => {
      await api.post("/invoices/", newInv);
    },
    onSuccess: () => {
      qc.invalidateQueries(["invoices"]);
      setShowForm(false);
    },
  });

  if (isLoading) return <p className="text-white">Cargando facturas…</p>;
  if (error) return <p className="text-red-500">Error al cargar facturas.</p>;

  // Funciones para manejar formulario (igual que antes)...
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };
  const handleLineChange = (idx, field, value) => {
    const newLines = [...formData.lines];
    newLines[idx][field] = value;
    setFormData((prev) => ({ ...prev, lines: newLines }));
  };
  const addLine = () => {
    setFormData((prev) => ({
      ...prev,
      lines: [...prev.lines, { product_id: "", qty: "" }],
    }));
  };
  const removeLine = (idx) => {
    const newLines = formData.lines.filter((_, i) => i !== idx);
    setFormData((prev) => ({ ...prev, lines: newLines }));
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = {
      company_id: Number(formData.company_id),
      customer_id: Number(formData.customer_id),
      lines: formData.lines.map((ln) => ({
        product_id: Number(ln.product_id),
        qty: Number(ln.qty),
      })),
    };
    createMutation.mutate(payload);
  };

  return (
    <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
      <div className="layout-content-container flex flex-col max-w-[960px] w-full">
        {/* ───────── Header (Título + Botón) ───────── */}
        <div className="flex flex-wrap justify-between items-center gap-3 p-4">
          <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">
            Invoices
          </p>
          <button
            onClick={() => setShowForm(true)}
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center rounded h-8 px-4 bg-[#20344b] text-white text-sm font-medium leading-normal hover:bg-[#2a4262]"
          >
            <span className="truncate">New invoice</span>
          </button>
        </div>

        {/* ───────── Filtros (Date, Customer, Amount) ───────── */}
        <div className="flex gap-3 p-3 flex-wrap pr-4">
          {["Date", "Customer", "Amount"].map((label) => (
            <button
              key={label}
              className="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded bg-[#20344b] px-2 hover:bg-[#2a4262]"
            >
              <p className="text-white text-sm font-medium leading-normal">
                {label}
              </p>
              {/* Ícono caret (svg inline) */}
              <div className="text-white">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20px"
                  height="20px"
                  fill="currentColor"
                  viewBox="0 0 256 256"
                >
                  <path d="M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80A8,8,0,0,1,53.66,90.34L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z" />
                </svg>
              </div>
            </button>
          ))}
        </div>

        {/* ───────── Tabla ───────── */}
        <div className="px-4 py-3" style={{ containerType: "inline-size" }}>
          <div className="flex overflow-hidden rounded border border-[#2e4a6b] bg-[#0f1924]">
            <table className="flex-1 border-collapse">
              {/* ─── Head ─── */}
              <thead>
                <tr className="bg-[#172536]">
                  <th className="column-120 px-4 py-3 text-left text-white w-[400px] text-sm font-medium leading-normal">
                    Date
                  </th>
                  <th className="column-240 px-4 py-3 text-left text-white w-[400px] text-sm font-medium leading-normal">
                    Customer
                  </th>
                  <th className="column-360 px-4 py-3 text-left text-white w-60 text-sm font-medium leading-normal">
                    Status
                  </th>
                  <th className="column-480 px-4 py-3 text-left text-white w-[400px] text-sm font-medium leading-normal">
                    Amount
                  </th>
                  <th className="column-600 px-4 py-3 text-left text-white w-[400px] text-sm font-medium leading-normal">
                    Due date
                  </th>
                  <th className="column-720 px-4 py-3 text-left text-[#8dabce] w-60 text-sm font-medium leading-normal">
                    Action
                  </th>
                </tr>
              </thead>
              {/* ─── Body ─── */}
              <tbody>
                {invoices.map((inv) => (
                  <tr key={inv.id} className="border-t border-t-[#2e4a6b]">
                    {/* Date */}
                    <td className="column-120 h-[72px] px-4 py-2 w-[400px] text-[#8dabce] text-sm font-normal leading-normal">
                      {/* Asumiendo que 'inv.date' viene en ISO, formateamos a MM/DD/YYYY */}
                      {new Date(inv.date).toLocaleDateString("en-US")}
                    </td>
                    {/* Customer (aquí podrías mapear inv.customer_id → nombre real, si lo tuvieras) */}
                    <td className="column-240 h-[72px] px-4 py-2 w-[400px] text-white text-sm font-normal leading-normal">
                      Customer #{inv.customer_id}
                    </td>
                    {/* Status (botón con texto) */}
                    <td className="column-360 h-[72px] px-4 py-2 w-60 text-sm font-normal leading-normal">
                      <button
                        className={`
                          flex w-full h-8 items-center justify-center rounded px-4 
                          text-sm font-medium leading-normal
                          ${
                            inv.status === "paid"
                              ? "bg-green-600 text-white hover:bg-green-700"
                              : inv.status === "overdue"
                              ? "bg-red-600 text-white hover:bg-red-700"
                              : "bg-[#20344b] text-white hover:bg-[#2a4262]"
                          }
                        `}
                      >
                        <span className="truncate">
                          {inv.status.charAt(0).toUpperCase() +
                            inv.status.slice(1)}
                        </span>
                      </button>
                    </td>
                    {/* Amount */}
                    <td className="column-480 h-[72px] px-4 py-2 w-[400px] text-[#8dabce] text-sm font-normal leading-normal">
                      ${inv.total.toFixed(2)}
                    </td>
                    {/* Due date (aquí asumo que inv.due_date existe; si no, puedes usar otro campo) */}
                    <td className="column-600 h-[72px] px-4 py-2 w-[400px] text-[#8dabce] text-sm font-normal leading-normal">
                      {inv.due_date
                        ? new Date(inv.due_date).toLocaleDateString("en-US")
                        : "-"}
                    </td>
                    {/* Action (“View” simple) */}
                    <td className="column-720 h-[72px] px-4 py-2 w-60 text-[#8dabce] text-sm font-bold leading-normal tracking-[0.015em] cursor-pointer hover:text-white">
                      View
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* ───────── Container Queries ───────── */}
          <style>
            {`
              @container (max-width: 120px) {
                .column-120 { display: none; }
              }
              @container (max-width: 240px) {
                .column-240 { display: none; }
              }
              @container (max-width: 360px) {
                .column-360 { display: none; }
              }
              @container (max-width: 480px) {
                .column-480 { display: none; }
              }
              @container (max-width: 600px) {
                .column-600 { display: none; }
              }
              @container (max-width: 720px) {
                .column-720 { display: none; }
              }
            `}
          </style>
        </div>
      </div>

      {/* ───────── Modal / Formulario para crear factura ───────── */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded shadow-lg w-96 max-h-[90vh] overflow-auto">
            <h2 className="text-xl font-semibold mb-4">Crear Factura</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block mb-1">Empresa ID</label>
                <input
                  type="number"
                  name="company_id"
                  value={formData.company_id}
                  onChange={handleInputChange}
                  className="w-full border px-2 py-1 rounded"
                  required
                />
              </div>
              <div>
                <label className="block mb-1">Cliente ID</label>
                <input
                  type="number"
                  name="customer_id"
                  value={formData.customer_id}
                  onChange={handleInputChange}
                  className="w-full border px-2 py-1 rounded"
                  required
                />
              </div>

              <h3 className="text-lg font-semibold mt-4">Líneas</h3>
              {formData.lines.map((ln, idx) => (
                <div key={idx} className="flex gap-2 items-end">
                  <div className="flex-1">
                    <label className="block text-sm">Producto ID</label>
                    <input
                      type="number"
                      value={ln.product_id}
                      onChange={(e) =>
                        handleLineChange(idx, "product_id", e.target.value)
                      }
                      className="w-full border px-2 py-1 rounded"
                      required
                    />
                  </div>
                  <div className="flex-1">
                    <label className="block text-sm">Qty</label>
                    <input
                      type="number"
                      value={ln.qty}
                      onChange={(e) =>
                        handleLineChange(idx, "qty", e.target.value)
                      }
                      className="w-full border px-2 py-1 rounded"
                      required
                    />
                  </div>
                  <button
                    type="button"
                    onClick={() => removeLine(idx)}
                    className="text-red-600 text-sm mt-5"
                  >
                    ×
                  </button>
                </div>
              ))}
              <button
                type="button"
                onClick={addLine}
                className="text-blue-600 hover:underline text-sm"
              >
                + Agregar línea
              </button>

              <div className="flex justify-end gap-2 mt-6">
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="px-4 py-2 border rounded hover:bg-gray-100"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-primary text-white rounded hover:bg-blue-700"
                  disabled={createMutation.isLoading}
                >
                  {createMutation.isLoading ? "Creando…" : "Crear"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}