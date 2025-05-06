SELECT w.Warehouse_Id AS Warehouse_Id,
       w.Name AS Warehouse_Name,
       COUNT(DISTINCT dis.Drug_Id) AS Drugs_Count,
       SUM(COALESCE(dis.Amount, 0)) AS Total_Drugs_Amount,
       COUNT(DISTINCT eis.Medical_Equipment_Id) AS Equipment_Count,
       SUM(COALESCE(eis.Amount, 0)) AS Total_Equipment_Amount
FROM Warehouse w
LEFT JOIN Drug_in_stock dis ON w.Warehouse_Id = dis.Warehouse_Id
LEFT JOIN Equipment_in_stock eis ON w.Warehouse_Id = eis.Warehouse_Id
GROUP BY w.Warehouse_Id
ORDER BY
    GREATEST(SUM(COALESCE(dis.Amount, 0)), SUM(COALESCE(eis.Amount, 0))) DESC,
    w.Warehouse_Id;