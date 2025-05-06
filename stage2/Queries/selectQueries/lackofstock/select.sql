-- שאילתה פשוטה יותר לפריטים עם מחסור במלאי
-- תרופות
SELECT d.Drug_Id AS Item_Id,
       d.Name AS Item_Name,
       'Drug' AS Item_Type,
       SUM(doi.Amount) AS Total_Ordered_Amount,
       (SELECT COALESCE(SUM(Amount), 0) FROM Drug_in_stock WHERE Drug_Id = d.Drug_Id) AS Total_Available_Amount,
       (SUM(doi.Amount) - (SELECT COALESCE(SUM(Amount), 0) FROM Drug_in_stock WHERE Drug_Id = d.Drug_Id)) AS Total_Shortage_Amount
FROM Drug d
JOIN Drug_order_item doi ON d.Drug_Id = doi.Drug_Id
GROUP BY d.Drug_Id, d.Name
HAVING SUM(doi.Amount) > (SELECT COALESCE(SUM(Amount), 0) FROM Drug_in_stock WHERE Drug_Id = d.Drug_Id)

UNION ALL

-- ציוד רפואי
SELECT me.Medical_Equipment_Id AS Item_Id,
       me.Name AS Item_Name,
       'Equipment' AS Item_Type,
       SUM(eoi.Amount) AS Total_Ordered_Amount,
       (SELECT COALESCE(SUM(Amount), 0) FROM Equipment_in_stock WHERE Medical_Equipment_Id = me.Medical_Equipment_Id) AS Total_Available_Amount,
       (SUM(eoi.Amount) - (SELECT COALESCE(SUM(Amount), 0) FROM Equipment_in_stock WHERE Medical_Equipment_Id = me.Medical_Equipment_Id)) AS Total_Shortage_Amount
FROM Medical_Equipment me
JOIN Equipment_order_item eoi ON me.Medical_Equipment_Id = eoi.Medical_Equipment_Id
GROUP BY me.Medical_Equipment_Id, me.Name
HAVING SUM(eoi.Amount) > (SELECT COALESCE(SUM(Amount), 0) FROM Equipment_in_stock WHERE Medical_Equipment_Id = me.Medical_Equipment_Id)

ORDER BY Total_Shortage_Amount DESC, Item_Type, Item_Id;