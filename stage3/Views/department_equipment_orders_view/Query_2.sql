SELECT 
    deo.department_id,
    d.name AS department_name,
    deo.equipment_name,
    deo.amount,
    deo.is_urgent,
    deo.status
FROM 
    department_equipment_orders_view deo
JOIN 
    public.department d ON deo.department_id = d.department_id
WHERE 
    d.emergency_level >= 3
ORDER BY 
    deo.is_urgent DESC,
    deo.amount DESC;
