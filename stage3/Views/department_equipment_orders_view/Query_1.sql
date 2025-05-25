SELECT 
    deo.department_id,
    d.name AS department_name,
    me.name AS equipment_name,
    SUM(deo.amount) AS total_requested,
    COUNT(*) FILTER (WHERE deo.is_urgent) AS urgent_count
FROM 
    department_equipment_orders_view deo
JOIN 
    department d ON deo.department_id = d.department_id
JOIN 
    medical_equipment me ON deo.medical_equipment_id = me.medical_equipment_id
WHERE 
    deo.status <> 'delivered'
GROUP BY 
    deo.department_id, d.name, me.name
ORDER BY 
    deo.department_id, me.name;
