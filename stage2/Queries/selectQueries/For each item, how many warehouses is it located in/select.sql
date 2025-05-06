SELECT 'Drug' AS Item_Type,
       d.Drug_Id AS Item_Id,
       d.Name AS Item_Name,
       COUNT(DISTINCT dis.Warehouse_Id) AS Warehouse_Count
FROM Drug d
LEFT JOIN Drug_in_stock dis ON d.Drug_Id = dis.Drug_Id
GROUP BY d.Drug_Id

UNION ALL

SELECT 'Equipment' AS Item_Type,
       me.Medical_Equipment_Id AS Item_Id,
       me.Name AS Item_Name,
       COUNT(DISTINCT eis.Warehouse_Id) AS Warehouse_Count
FROM Medical_Equipment me
LEFT JOIN Equipment_in_stock eis ON me.Medical_Equipment_Id = eis.Medical_Equipment_Id
GROUP BY me.Medical_Equipment_Id

ORDER BY Warehouse_Count DESC, Item_Type, Item_Id;