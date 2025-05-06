-- שאילתת תרופות
SELECT w.Warehouse_Id AS Warehouse_Id,
       w.Name AS Warehouse_Name, 
       'Drug' AS Item_Type,
       d.Drug_Id AS Item_Id,
       d.Name AS Item_Name,
       SUM(doi.Amount) AS Order_Amount,
       dis.Amount AS Stock_Amount
FROM Logistic_worker lw
JOIN Has_access ha ON lw.Logistic_worker_Id = ha.Logistic_worker_Id
JOIN Warehouse w ON ha.Warehouse_Id = w.Warehouse_Id
JOIN Works_for wf ON lw.Logistic_worker_Id = wf.Logistic_worker_Id
JOIN "Order" o ON wf.Department_Id = o.Department_Id
JOIN Drug_order_item doi ON o.Order_Id = doi.Order_Id AND o.Department_Id = doi.Department_Id
JOIN Drug d ON doi.Drug_Id = d.Drug_Id
JOIN Drug_in_stock dis ON d.Drug_Id = dis.Drug_Id AND w.Warehouse_Id = dis.Warehouse_Id
WHERE lw.Logistic_worker_Id = 1
AND doi.Status = 'pending'
GROUP BY w.Warehouse_Id, d.Drug_Id, dis.Amount

UNION ALL

-- שאילתת ציוד
SELECT w.Warehouse_Id AS Warehouse_Id,
       w.Name AS Warehouse_Name, 
       'Equipment' AS Item_Type,
       me.Medical_Equipment_Id AS Item_Id,
       me.Name AS Item_Name,
       SUM(eoi.Amount) AS Order_Amount,
       eis.Amount AS Stock_Amount
FROM Logistic_worker lw
JOIN Has_access ha ON lw.Logistic_worker_Id = ha.Logistic_worker_Id
JOIN Warehouse w ON ha.Warehouse_Id = w.Warehouse_Id
JOIN Works_for wf ON lw.Logistic_worker_Id = wf.Logistic_worker_Id
JOIN "Order" o ON wf.Department_Id = o.Department_Id
JOIN Equipment_order_item eoi ON o.Order_Id = eoi.Order_Id AND o.Department_Id = eoi.Department_Id
JOIN Medical_Equipment me ON eoi.Medical_Equipment_Id = me.Medical_Equipment_Id
JOIN Equipment_in_stock eis ON me.Medical_Equipment_Id = eis.Medical_Equipment_Id AND w.Warehouse_Id = eis.Warehouse_Id
WHERE lw.Logistic_worker_Id = 1
AND eoi.Status = 'pending'
GROUP BY w.Warehouse_Id, me.Medical_Equipment_Id, eis.Amount

ORDER BY Warehouse_Id, Item_Type, Item_Id;