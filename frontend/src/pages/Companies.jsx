import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useApi } from "../hooks/useApi";
import { useSortableData } from "../hooks/useSortableData";

export default function Companies() {
  const qc = useQueryClient();
  const api = useApi();

  // 1️⃣ Traer lista de compañías
  const {
    data: companies = [],
    isLoading,
  } = useQuery({
    queryKey: ["companies"],
    queryFn: async () => (await api.get("/companies/")).data,
  });

  // hook de ordenamiento
  const { items: sortedCompanies, requestSort, sortConfig } =
    useSortableData(companies);

  const getClassNamesFor = (name) =>
    sortConfig?.key === name
      ? sortConfig.direction === "ascending"
        ? " ▲"
        : " ▼"
      : "";

  // 2️⃣ Eliminar
  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(`/companies/${id}`),
    onSuccess: () => qc.invalidateQueries(["companies"]),
  });
  // 3️⃣ Crear demo
  const createMutation = useMutation({
    mutationFn: () =>
      api.post("/companies/", { name: "Demo Corp", industry: "Technology" }),
    onSuccess: () => qc.invalidateQueries(["companies"]),
  });

  return (
    <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
      <div className="layout-content-container flex flex-col max-w-[960px] w-full">
        {/* Header */}
        <div className="flex flex-wrap justify-between items-center gap-3 p-4">
          <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">
            Compañías
          </p>
          <button
            onClick={() => createMutation.mutate()}
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center rounded h-8 px-4 bg-[#20344b] text-white text-sm font-medium leading-normal hover:bg-[#2a4262]"
          >
            + Nuevo
          </button>
        </div>

        {/* Tabla */}
        <div className="px-4 py-3" style={{ containerType: "inline-size" }}>
          <div className="flex overflow-hidden rounded border border-[#2e4a6b] bg-[#0f1924]">
            <table className="flex-1 border-collapse">
              <thead>
                <tr className="bg-[#172536]">
                  <th
                    onClick={() => requestSort("name")}
                    className="column-240 px-4 py-3 text-left text-white w-[400px] text-sm font-medium leading-normal cursor-pointer"
                  >
                    Nombre{getClassNamesFor("name")}
                  </th>
                  <th
                    onClick={() => requestSort("industry")}
                    className="column-480 px-4 py-3 text-left text-white w-[400px] text-sm font-medium leading-normal cursor-pointer"
                  >
                    Industria{getClassNamesFor("industry")}
                  </th>
                  <th className="column-720 px-4 py-3 text-left text-[#8dabce] w-60 text-sm font-medium leading-normal">
                    Acción
                  </th>
                  <th
                    onClick={() => requestSort("id")}
                    className="column-120 px-4 py-3 text-left text-white w-24 text-sm font-medium leading-normal cursor-pointer"
                  >
                    ID{getClassNamesFor("id")}
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
                ) : sortedCompanies.length > 0 ? (
                  sortedCompanies.map((row) => (
                    <tr key={row.id} className="border-t border-t-[#2e4a6b]">
                      <td className="column-240 h-[72px] px-4 py-2 text-white text-sm">
                        {row.name}
                      </td>
                      <td className="column-480 h-[72px] px-4 py-2 text-[#8dabce] text-sm">
                        {row.industry}
                      </td>
                      <td className="column-720 h-[72px] px-4 py-2 text-sm">
                        <button
                          onClick={() => deleteMutation.mutate(row.id)}
                          className="w-full h-8 flex items-center justify-center rounded bg-[#20344b] text-white text-sm hover:bg-[#2a4262]"
                        >
                          Borrar
                        </button>
                      </td>
                      <td className="column-120 h-[72px] px-4 py-2 text-[#8dabce] text-sm">
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

          {/* container queries */}
          <style>{`
            @container (max-width:240px) { .column-240{display:none} }
            @container (max-width:480px) { .column-480{display:none} }
            @container (max-width:720px) { .column-720{display:none} }
            @container (max-width:960px) { .column-120{display:none} }
          `}</style>
        </div>
      </div>
    </div>
  );
}