// src/pages/Invoices.jsx
import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/axios";
import TableBase from "../components/TableBase";

export default function Invoices() {
  const qc = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    company_id: "",
    customer_id: "",
    lines: [{ product_id: "", qty: "" }],
  });

  // 1️⃣ Traer lista de facturas
  const { data: invoices, isLoading, error } = useQuery({ // Un solo objeto como argumento
    queryKey: ["invoices"],
    queryFn: async () => {
      const res = await api.get("/invoices/");
      return res.data;
    }
    // Aquí puedes añadir otras opciones de query si las necesitas
  });

  // 2️⃣ Mutación: crear factura
  const createMutation = useMutation({ // Un solo objeto como argumento
    mutationFn: async (newInv) => { // La función ahora es una propiedad 'mutationFn'
      await api.post("/invoices/", newInv);
    },
    onSuccess: () => { // Las opciones van en el mismo objeto
      qc.invalidateQueries(["invoices"]);
      setShowForm(false);
    },
    // Aquí puedes añadir otras opciones de mutación si las necesitas
  });

  if (isLoading) return <p>Cargando facturas…</p>;
  if (error) return <p>Error al cargar facturas.</p>;

  const columns = [
    { key: "id", header: "ID" },
    { key: "date", header: "Fecha" },
    { key: "company_id", header: "Empresa ID" },
    { key: "customer_id", header: "Cliente ID" },
    { key: "subtotal", header: "Subtotal" },
    { key: "tax", header: "Impuesto" },
    { key: "total", header: "Total" },
    { key: "status", header: "Estado" },
    {
      key: "has_pdf",
      header: "PDF",
      render: (row) =>
        row.has_pdf ? (
          <button
            onClick={() =>
              window.open(`http://localhost:8000/invoices/${row.id}/pdf`)
            }
            className="text-blue-600 hover:underline"
          >
            Descargar
          </button>
        ) : (
          <span className="text-gray-500">Sin PDF</span>
        ),
    },
  ];

  // Funciones para manejar el formulario:
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
    // Convierte strings a números
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
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-semibold">Facturas</h1>
        <button
          onClick={() => setShowForm(true)}
          className="bg-primary text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          + Nueva Factura
        </button>
      </div>

      <TableBase data={invoices || []} columns={columns} />

      {/* Modal / Formulario para crear factura */}
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