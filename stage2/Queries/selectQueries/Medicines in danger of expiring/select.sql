SELECT d.Drug_Id AS Drug_Id,
       d.Name AS Drug_Name,
       dis.Warehouse_Id AS Warehouse_Id,
       w.Name AS Warehouse_Name,
       dis.Since AS Entry_Date,
       dis.Amount AS Amount,
       (CURRENT_DATE - dis.Since) AS Days_Since_Entry,
       d.Shelf_life AS Shelf_Life_Days,
       (d.Shelf_life - (CURRENT_DATE - dis.Since)) AS Days_Until_Expiry
FROM Drug d
JOIN Drug_in_stock dis ON d.Drug_Id = dis.Drug_Id
JOIN Warehouse w ON dis.Warehouse_Id = w.Warehouse_Id
WHERE (CURRENT_DATE - dis.Since) > (d.Shelf_life - 30)  -- פחות מחודש לתפוגה
  AND d.Shelf_life > 0  -- רק תרופות עם חיי מדף מוגדרים
ORDER BY Days_Until_Expiry, d.Drug_Id, dis.Warehouse_Id;