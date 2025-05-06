SELECT d.Department_Id AS Department_Id,
       d.Name AS Department_Name,
       COUNT(CASE WHEN doi.Is_urgent = TRUE THEN 1 END) AS Urgent_Drug_Items_Count,
       COUNT(CASE WHEN eoi.Is_urgent = TRUE THEN 1 END) AS Urgent_Equipment_Items_Count,
       (COUNT(CASE WHEN doi.Is_urgent = TRUE THEN 1 END) + 
        COUNT(CASE WHEN eoi.Is_urgent = TRUE THEN 1 END)) AS Total_Urgent_Items_Count
FROM Department d
LEFT JOIN "Order" o ON d.Department_Id = o.Department_Id
LEFT JOIN Drug_order_item doi ON o.Department_Id = doi.Department_Id AND o.Order_Id = doi.Order_Id
LEFT JOIN Equipment_order_item eoi ON o.Department_Id = eoi.Department_Id AND o.Order_Id = eoi.Order_Id
GROUP BY d.Department_Id
ORDER BY Total_Urgent_Items_Count DESC, d.Department_Id;