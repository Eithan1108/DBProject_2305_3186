SELECT lw.Logistic_worker_Id AS Worker_Id,
       lw.Name AS Worker_Name,
       COUNT(DISTINCT ha.Warehouse_Id) AS Accessible_Warehouses_Count,
       STRING_AGG(w.Name, ', ') AS Accessible_Warehouses
FROM Logistic_worker lw
LEFT JOIN Has_access ha ON lw.Logistic_worker_Id = ha.Logistic_worker_Id
LEFT JOIN Warehouse w ON ha.Warehouse_Id = w.Warehouse_Id
GROUP BY lw.Logistic_worker_Id
ORDER BY Accessible_Warehouses_Count DESC, lw.Logistic_worker_Id;