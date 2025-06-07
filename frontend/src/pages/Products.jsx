// src/pages/Products.jsx
import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useApi } from '../hooks/useApi';

export default function Products() {
  const qc = useQueryClient();
  const api = useApi();
  // 1️⃣ Traer lista de productos
  const {
    data: products,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["products"],
    queryFn: async () => {
      const res = await api.get("/products/");
      return res.data;
    },
  });

  // 2️⃣ Mutación: eliminar producto
  const deleteMutation = useMutation({
    mutationFn: async (id) => {
      await api.delete(`/products/${id}`);
    },
    onSuccess: () => qc.invalidateQueries(["products"]),
  });

  // 3️⃣ Mutación: crear producto demo
  const createMutation = useMutation({
    mutationFn: async () => {
      await api.post("/products/", {
        company_id: 1,
        sku: "PRD-001",
        name: "Servicio Demo",
        type: "service",
        unit_price: 100.0,
        tax_rate: 0.07,
      });
    },
    onSuccess: () => qc.invalidateQueries(["products"]),
  });

  if (isLoading)
    return (
      <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
        <p className="text-white">Cargando productos…</p>
      </div>
    );
  if (error)
    return (
      <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
        <p className="text-red-500">Error al cargar productos.</p>
      </div>
    );

  return (
    <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
      <div className="layout-content-container flex flex-col max-w-[960px] w-full">
        {/* ───────── Header (Título + Botón) ───────── */}
        <div className="flex flex-wrap justify-between items-center gap-3 p-4">
          <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">
            Productos
          </p>
          <button
            onClick={() => createMutation.mutate()}
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center rounded h-8 px-4 bg-[#20344b] text-white text-sm font-medium leading-normal hover:bg-[#2a4262]"
          >
            <span className="truncate">+ Nuevo</span>
          </button>
        </div>

        {/* ───────── Tabla de Productos ───────── */}
        <div className="px-4 py-3" style={{ containerType: "inline-size" }}>
          <div className="flex overflow-x-auto rounded border border-[#2e4a6b] bg-[#0f1924]">
            <table className="flex-1 border-collapse min-w-full">
              {/* ─── Head ─── */}
              <thead>
                <tr className="bg-[#172536]">
                  <th className="column-sku px-4 py-3 text-left text-white w-[200px] text-sm font-medium leading-normal">
                    SKU
                  </th>
                  <th className="column-name px-4 py-3 text-left text-white w-[240px] text-sm font-medium leading-normal">
                    Nombre
                  </th>
                  <th className="column-price px-4 py-3 text-left text-white w-[160px] text-sm font-medium leading-normal">
                    Precio&nbsp;Unitario
                  </th>
                  <th className="column-tax px-4 py-3 text-left text-white w-[120px] text-sm font-medium leading-normal">
                    Impuesto
                  </th>
                  <th className="column-type px-4 py-3 text-left text-[#8dabce] w-[120px] text-sm font-medium leading-normal">
                    Tipo
                  </th>
                  <th className="column-company px-4 py-3 text-left text-[#8dabce] w-[160px] text-sm font-medium leading-normal">
                    Empresa&nbsp;ID
                  </th>
                  <th className="column-actions px-4 py-3 text-left text-[#8dabce] w-60 text-sm font-medium leading-normal">
                    Acciones
                  </th>
                  <th className="column-id px-4 py-3 text-left text-[#8dabce] w-16 text-sm font-medium leading-normal">
                    ID
                  </th>
                </tr>
              </thead>

              {/* ─── Body ─── */}
              <tbody>
                {products.map((item) => (
                  <tr key={item.id} className="border-t border-t-[#2e4a6b]">
                    {/* SKU */}
                    <td className="column-sku h-[60px] px-4 py-2 w-[200px] text-[#8dabce] text-sm font-normal leading-normal truncate">
                      {item.sku}
                    </td>
                    {/* Nombre */}
                    <td className="column-name h-[60px] px-4 py-2 w-[240px] text-white text-sm font-normal leading-normal truncate">
                      {item.name}
                    </td>
                    {/* Precio Unitario */}
                    <td className="column-price h-[60px] px-4 py-2 w-[160px] text-[#8dabce] text-sm font-normal leading-normal">
                      ${item.unit_price.toFixed(2)}
                    </td>
                    {/* Impuesto */}
                    <td className="column-tax h-[60px] px-4 py-2 w-[120px] text-[#8dabce] text-sm font-normal leading-normal">
                      {(item.tax_rate * 100).toFixed(1)}%
                    </td>
                    {/* Tipo */}
                    <td className="column-type h-[60px] px-4 py-2 w-[120px] text-[#8dabce] text-sm font-normal leading-normal truncate">
                      {item.type}
                    </td>
                    {/* Empresa ID */}
                    <td className="column-company h-[60px] px-4 py-2 w-[160px] text-[#8dabce] text-sm font-normal leading-normal">
                      {item.company_id}
                    </td>
                    {/* Acciones: botón “Borrar” */}
                    <td className="column-actions h-[60px] px-4 py-2 w-60 text-sm font-normal leading-normal">
                      <button
                        onClick={() => deleteMutation.mutate(item.id)}
                        className="flex w-full h-8 items-center justify-center rounded px-4 bg-[#20344b] text-white text-sm font-medium leading-normal hover:bg-[#2a4262]"
                      >
                        <span className="truncate">Borrar</span>
                      </button>
                    </td>
                    {/* ID */}
                    <td className="column-id h-[60px] px-4 py-2 w-16 text-[#8dabce] text-sm font-normal leading-normal">
                      {item.id}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* ───────── Container Queries ───────── */}
          <style>
            {`
              /* Ocultar ID en contenedores < 960px */
              @container (max-width: 960px) {
                .column-id { display: none; }
              }
              /* Ocultar “Empresa ID” en contenedores < 800px */
              @container (max-width: 800px) {
                .column-company { display: none; }
              }
              /* Ocultar “Tipo” en contenedores < 640px */
              @container (max-width: 640px) {
                .column-type { display: none; }
              }
              /* Ocultar “Impuesto” en contenedores < 480px */
              @container (max-width: 480px) {
                .column-tax { display: none; }
              }
              /* Ocultar “Precio Unitario” en contenedores < 360px */
              @container (max-width: 360px) {
                .column-price { display: none; }
              }
            `}
          </style>
        </div>
      </div>
    </div>
  );
}