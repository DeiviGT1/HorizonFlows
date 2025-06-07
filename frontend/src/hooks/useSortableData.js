// src/hooks/useSortableData.js
import { useState, useMemo } from "react";

export function useSortableData(items, config = null) {
  const [sortConfig, setSortConfig] = useState(config);

  const sortedItems = useMemo(() => {
    if (!items) return [];
    const sortableItems = [...items];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        const aKey = a[sortConfig.key];
        const bKey = b[sortConfig.key];
        if (aKey < bKey) return sortConfig.direction === "ascending" ? -1 : 1;
        if (aKey > bKey) return sortConfig.direction === "ascending" ? 1 : -1;
        return 0;
      });
    }
    return sortableItems;
  }, [items, sortConfig]);

  const requestSort = (key) => {
    let direction = "ascending";
    if (
      sortConfig &&
      sortConfig.key === key &&
      sortConfig.direction === "ascending"
    ) {
      direction = "descending";
    }
    setSortConfig({ key, direction });
  };

  return { items: sortedItems, requestSort, sortConfig };
}