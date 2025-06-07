import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useApi } from "../hooks/useApi";
import { useSortableData } from "../hooks/useSortableData";

export default function Invoices() {
  const qc = useQueryClient();
  const api = useApi();
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    company_id: "", customer_id: "", lines: [{ product_id: "", qty: "" }],
  });

  // 1️⃣ Traer facturas
  const {
    data: invoices = [],
    isLoading,
  } = useQuery({
    queryKey: ["invoices"],
    queryFn: async () => (await api.get("/invoices/")).data,
  });

  // hook de orden
  const { items: sortedInvoices, requestSort, sortConfig } =
    useSortableData(invoices);
  const getClassNamesFor = (name) =>
    sortConfig?.key === name
      ? sortConfig.direction === "ascending"
        ? " ▲"
        : " ▼"
      : "";

  // 2️⃣ Crear factura
  const createMutation = useMutation({
    mutationFn: (newInv) => api.post("/invoices/", newInv),
    onSuccess: () => {
      qc.invalidateQueries(["invoices"]);
      setShowForm(false);
    },
  });

  // handlers form…
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((p) => ({ ...p, [name]: value }));
  };
  const handleLineChange = (idx, field, value) => {
    const nl = [...formData.lines];
    nl[idx][field] = value;
    setFormData((p) => ({ ...p, lines: nl }));
  };
  const addLine = () =>
    setFormData((p) => ({
      ...p,
      lines: [...p.lines, { product_id: "", qty: "" }],
    }));
  const removeLine = (idx) =>
    setFormData((p) => ({
      ...p,
      lines: p.lines.filter((_, i) => i !== idx),
    }));
  const handleSubmit = (e) => {
    e.preventDefault();
    createMutation.mutate({
      company_id: Number(formData.company_id),
      customer_id: Number(formData.customer_id),
      lines: formData.lines.map((ln) => ({
        product_id: Number(ln.product_id),
        qty: Number(ln.qty),
      })),
    });
  };

  return (
    <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
      <div className="layout-content-container flex flex-col max-w-[960px] w-full">
        {/* Header */}
        <div className="flex flex-wrap justify-between items-center gap-3 p-4">
          <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">
            Facturas
          </p>
          <button
            onClick={() => setShowForm(true)}
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center rounded h-8 px-4 bg-[#20344b] text-white text-sm hover:bg-[#2a4262]"
          >
            Nueva factura
          </button>
        </div>

        {/* Tabla */}
        <div className="px-4 py-3" style={{ containerType: "inline-size" }}>
          <div className="flex overflow-hidden rounded border border-[#2e4a6b] bg-[#0f1924]">
            <table className="flex-1 border-collapse">
              <thead>
                <tr className="bg-[#172536]">
                  <th
                    onClick={() => requestSort("date")}
                    className="column-120 px-4 py-3 text-left text-white w-[400px] cursor-pointer"
                  >
                    Fecha{getClassNamesFor("date")}
                  </th>
                  <th
                    onClick={() => requestSort("customer_id")}
                    className="column-240 px-4 py-3 text-left text-white w-[400px] cursor-pointer"
                  >
                    Cliente{getClassNamesFor("customer_id")}
                  </th>
                  <th
                    onClick={() => requestSort("status")}
                    className="column-360 px-4 py-3 text-left text-white w-60 cursor-pointer"
                  >
                    Estado{getClassNamesFor("status")}
                  </th>
                  <th
                    onClick={() => requestSort("total")}
                    className="column-480 px-4 py-3 text-left text-white w-[400px] cursor-pointer"
                  >
                    Monto{getClassNamesFor("total")}
                  </th>
                  <th className="column-600 px-4 py-3 text-left text-white w-[400px]">
                    Vence
                  </th>
                  <th className="column-720 px-4 py-3 text-left text-[#8dabce] w-60">
                    Acción
                  </th>
                </tr>
              </thead>
              <tbody>
                {isLoading ? (
                  <tr>
                    <td colSpan={6} className="px-4 py-6 text-center text-white">
                      Cargando…
                    </td>
                  </tr>
                ) : sortedInvoices.length > 0 ? (
                  sortedInvoices.map((inv) => (
                    <tr key={inv.id} className="border-t border-t-[#2e4a6b]">
                      <td className="column-120 px-4 py-2 text-[#8dabce] text-sm">
                        {new Date(inv.date).toLocaleDateString()}
                      </td>
                      <td className="column-240 px-4 py-2 text-white text-sm">
                        Cliente #{inv.customer_id}
                      </td>
                      <td className="column-360 px-4 py-2 text-sm">
                        <button
                          className={`flex w-full h-8 items-center justify-center rounded px-4 text-sm ${
                            inv.status === "paid"
                              ? "bg-green-600 text-white"
                              : inv.status === "overdue"
                              ? "bg-red-600 text-white"
                              : "bg-[#20344b] text-white"
                          }`}
                        >
                          {inv.status.charAt(0).toUpperCase() + inv.status.slice(1)}
                        </button>
                      </td>
                      <td className="column-480 px-4 py-2 text-[#8dabce] text-sm">
                        ${inv.total.toFixed(2)}
                      </td>
                      <td className="column-600 px-4 py-2 text-[#8dabce] text-sm">
                        {inv.due_date
                          ? new Date(inv.due_date).toLocaleDateString()
                          : "-"}
                      </td>
                      <td className="column-720 px-4 py-2 text-[#8dabce] text-sm">Ver</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={6} className="px-4 py-6 text-center text-[#8dabce]">
                      No se encontraron facturas
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          <style>{`
            @container (max-width:120px){.column-120{display:none}}
            @container (max-width:240px){.column-240{display:none}}
            @container (max-width:360px){.column-360{display:none}}
            @container (max-width:480px){.column-480{display:none}}
          `}</style>
        </div>
      </div>

      {/* Form modal omitido */}
    </div>
  );
}