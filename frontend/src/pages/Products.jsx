// src/pages/Products.jsx (Updated)
import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useApi } from "../hooks/useApi";
import { useSortableData } from "../hooks/useSortableData";
import { useCompany } from "../context/CompanyContext"; // 👈 IMPORT

export default function Products() {
  const qc = useQueryClient();
  const api = useApi();
  const { currentCompany } = useCompany(); // 👈 USE THE CONTEXT

  const { data: products = [], isLoading } = useQuery({
    queryKey: ["products", currentCompany?.id], // Add company ID to queryKey
    queryFn: async () => (await api.get("/products/")).data,
    enabled: !!currentCompany, // Only run query if company is loaded
  });

  const { items: sortedProducts, requestSort, sortConfig } = useSortableData(products);
  const getClassNamesFor = (name) =>
    sortConfig?.key === name ? (sortConfig.direction === "ascending" ? " ▲" : " ▼") : "";

  // 2️⃣ Eliminar
  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(`/products/${id}`),
    onSuccess: () => qc.invalidateQueries(["products"]),
  });
  // 3️⃣ Crear demo
  const createMutation = useMutation({
    mutationFn: (newProduct) => api.post("/products/", newProduct),
    onSuccess: () => qc.invalidateQueries(["products", currentCompany?.id]),
  });

  const handleCreateDemo = () => {
    if (!currentCompany) return; // Guard clause
    createMutation.mutate({
      // 👇 FIX THE HARDCODED ID
      company_id: currentCompany.id,
      sku: `SKU-${Math.floor(Math.random() * 1000)}`,
      name: "Servicio Demo",
      type: "service",
      unit_price: 150.0,
      tax_rate: 0.07,
    })
  }

  return (
    <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
      <div className="layout-content-container flex flex-col max-w-[960px] w-full">
        <div className="flex flex-wrap justify-between items-center gap-3 p-4">
          <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">
            {currentCompany?.name}: Productos
          </p>
          <button
            onClick={handleCreateDemo} // Use the new handler
            className="..."
          >
            + Nuevo
          </button>
        </div>

        {/* Tabla */}
        <div className="px-4 py-3" style={{ containerType: "inline-size" }}>
          <div className="flex overflow-x-auto rounded border border-[#2e4a6b] bg-[#0f1924]">
            <table className="flex-1 border-collapse min-w-full">
              <thead>
                <tr className="bg-[#172536]">
                  <th
                    onClick={() => requestSort("sku")}
                    className="column-sku px-4 py-3 text-left text-white w-[200px] cursor-pointer"
                  >
                    SKU{getClassNamesFor("sku")}
                  </th>
                  <th
                    onClick={() => requestSort("name")}
                    className="column-name px-4 py-3 text-left text-white w-[240px] cursor-pointer"
                  >
                    Nombre{getClassNamesFor("name")}
                  </th>
                  <th
                    onClick={() => requestSort("unit_price")}
                    className="column-price px-4 py-3 text-left text-white w-[160px] cursor-pointer"
                  >
                    Precio Unitario{getClassNamesFor("unit_price")}
                  </th>
                  <th
                    onClick={() => requestSort("tax_rate")}
                    className="column-tax px-4 py-3 text-left text-white w-[120px] cursor-pointer"
                  >
                    Impuesto{getClassNamesFor("tax_rate")}
                  </th>
                  <th
                    onClick={() => requestSort("type")}
                    className="column-type px-4 py-3 text-left text-[#8dabce] w-[120px] cursor-pointer"
                  >
                    Tipo{getClassNamesFor("type")}
                  </th>
                  <th
                    onClick={() => requestSort("company_id")}
                    className="column-company px-4 py-3 text-left text-[#8dabce] w-[160px] cursor-pointer"
                  >
                    Empresa ID{getClassNamesFor("company_id")}
                  </th>
                  <th className="column-actions px-4 py-3 text-left text-[#8dabce] w-60">
                    Acciones
                  </th>
                  <th
                    onClick={() => requestSort("id")}
                    className="column-id px-4 py-3 text-left text-[#8dabce] w-16 cursor-pointer"
                  >
                    ID{getClassNamesFor("id")}
                  </th>
                </tr>
              </thead>
              <tbody>
                {isLoading ? (
                  <tr>
                    <td colSpan={8} className="px-4 py-6 text-center text-white">
                      Cargando…
                    </td>
                  </tr>
                ) : sortedProducts.length > 0 ? (
                  sortedProducts.map((item) => (
                    <tr key={item.id} className="border-t border-t-[#2e4a6b]">
                      <td className="column-sku px-4 py-2 text-[#8dabce] truncate">
                        {item.sku}
                      </td>
                      <td className="column-name px-4 py-2 text-white truncate">
                        {item.name}
                      </td>
                      <td className="column-price px-4 py-2 text-[#8dabce]">
                        ${item.unit_price.toFixed(2)}
                      </td>
                      <td className="column-tax px-4 py-2 text-[#8dabce]">
                        {(item.tax_rate * 100).toFixed(1)}%
                      </td>
                      <td className="column-type px-4 py-2 text-[#8dabce] truncate">
                        {item.type}
                      </td>
                      <td className="column-company px-4 py-2 text-[#8dabce]">
                        {item.company_id}
                      </td>
                      <td className="column-actions px-4 py-2">
                        <button
                          onClick={() => deleteMutation.mutate(item.id)}
                          className="w-full h-8 flex items-center justify-center rounded bg-[#20344b] text-white text-sm hover:bg-[#2a4262]"
                        >
                          Borrar
                        </button>
                      </td>
                      <td className="column-id px-4 py-2 text-[#8dabce]">
                        {item.id}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={8} className="px-4 py-6 text-center text-[#8dabce]">
                      No se encontraron productos
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {/* container queries */}
          <style>{`
            @container (max-width:360px) {.column-price{display:none}}
            @container (max-width:480px) {.column-tax{display:none}}
            @container (max-width:640px) {.column-type{display:none}}
            @container (max-width:800px) {.column-company{display:none}}
            @container (max-width:960px) {.column-id{display:none}}
          `}</style>
        </div>
      </div>
    </div>
  );
}