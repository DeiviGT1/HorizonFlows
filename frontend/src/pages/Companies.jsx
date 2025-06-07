// src/pages/Companies.jsx
import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useApi } from "../hooks/useApi";

export default function Companies() {
  const qc = useQueryClient();
  const api = useApi();

  // 1️⃣ Traer lista de compañías
  const {
    data: companies = [],      // <- default a [] si error o sin datos
    isLoading,                  // spinner
    // no usamos `error` para cortar la UI; lo podemos loguear si quieres
  } = useQuery({
    queryKey: ["companies"],
    queryFn: async () => {
      const res = await api.get("/companies/");
      return res.data;
    },
  });

  // 2️⃣ Mutación: eliminar compañía
  const deleteMutation = useMutation({
    mutationFn: async (id) => {
      await api.delete(`/companies/${id}`);
    },
    onSuccess: () => qc.invalidateQueries(["companies"]),
  });

  // 3️⃣ Mutación: crear compañía demo
  const createMutation = useMutation({
    mutationFn: async () => {
      await api.post("/companies/", {
        name: "Demo Corp",
        industry: "Technology",
      });
    },
    onSuccess: () => qc.invalidateQueries(["companies"]),
  });

  return (
    <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
      <div className="layout-content-container flex flex-col max-w-[960px] w-full">
        {/* ───────── Header ───────── */}
        <div className="flex flex-wrap justify-between items-center gap-3 p-4">
          <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">
            Compañías
          </p>
          <button
            onClick={() => createMutation.mutate()}
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center rounded h-8 px-4 bg-[#20344b] text-white text-sm font-medium leading-normal hover:bg-[#2a4262]"
          >
            <span className="truncate">+ Nuevo</span>
          </button>
        </div>

        {/* ───────── Tabla ───────── */}
        <div className="px-4 py-3" style={{ containerType: "inline-size" }}>
          <div className="flex overflow-hidden rounded border border-[#2e4a6b] bg-[#0f1924]">
            <table className="flex-1 border-collapse">
              <thead>
                <tr className="bg-[#172536]">
                  <th className="column-240 px-4 py-3 text-left text-white w-[400px] text-sm font-medium leading-normal">
                    Nombre
                  </th>
                  <th className="column-480 px-4 py-3 text-left text-white w-[400px] text-sm font-medium leading-normal">
                    Industria
                  </th>
                  <th className="column-720 px-4 py-3 text-left text-[#8dabce] w-60 text-sm font-medium leading-normal">
                    Acción
                  </th>
                  <th className="column-120 px-4 py-3 text-left text-white w-24 text-sm font-medium leading-normal">
                    ID
                  </th>
                </tr>
              </thead>
              <tbody>
                {isLoading ? (
                  <tr>
                    <td colSpan={4} className="px-4 py-6 text-center text-white">
                      Cargando…
                    </td>
                  </tr>
                ) : companies.length > 0 ? (
                  companies.map((row) => (
                    <tr key={row.id} className="border-t border-t-[#2e4a6b]">
                      <td className="column-240 h-[72px] px-4 py-2 w-[400px] text-white text-sm font-normal leading-normal">
                        {row.name}
                      </td>
                      <td className="column-480 h-[72px] px-4 py-2 w-[400px] text-[#8dabce] text-sm font-normal leading-normal">
                        {row.industry}
                      </td>
                      <td className="column-720 h-[72px] px-4 py-2 w-60 text-sm font-normal leading-normal">
                        <button
                          onClick={() => deleteMutation.mutate(row.id)}
                          className="flex w-full h-8 items-center justify-center rounded px-4 bg-[#20344b] text-white text-sm font-medium leading-normal hover:bg-[#2a4262]"
                        >
                          <span className="truncate">Borrar</span>
                        </button>
                      </td>
                      <td className="column-120 h-[72px] px-4 py-2 w-24 text-[#8dabce] text-sm font-normal leading-normal">
                        {row.id}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={4} className="px-4 py-6 text-center text-[#8dabce]">
                      No se encontraron compañías
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {/* ───────── Container Queries ───────── */}
          <style>
            {`
              @container (max-width: 240px) {
                .column-240 { display: none; }
              }
              @container (max-width: 480px) {
                .column-480 { display: none; }
              }
              @container (max-width: 720px) {
                .column-720 { display: none; }
              }
              @container (max-width: 960px) {
                .column-120 { display: none; }
              }
            `}
          </style>
        </div>
      </div>
    </div>
  );
}