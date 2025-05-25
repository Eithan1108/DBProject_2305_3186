 SELECT o.order_id,
    o.department_id,
    d.name AS department_name,
    eoi.medical_equipment_id,
    me.name AS equipment_name,
    eoi.amount,
    eoi.is_urgent,
    eoi.need_to_be_built,
    eoi.status
   FROM "Order" o
     JOIN department d ON o.department_id = d.department_id
     JOIN equipment_order_item eoi ON o.order_id = eoi.order_id AND o.department_id = eoi.department_id
     JOIN medical_equipment me ON eoi.medical_equipment_id = me.medical_equipment_id;