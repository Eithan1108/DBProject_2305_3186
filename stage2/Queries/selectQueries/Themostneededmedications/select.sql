SELECT d.Drug_Id AS Drug_Id,
       d.Name AS Drug_Name,
       COUNT(DISTINCT doi.Order_Id) AS Orders_Count,
       SUM(doi.Amount) AS Total_Amount_Ordered
FROM Drug d
JOIN Drug_order_item doi ON d.Drug_Id = doi.Drug_Id
GROUP BY d.Drug_Id
ORDER BY Total_Amount_Ordered DESC, d.Drug_Id;