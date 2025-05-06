DELETE FROM Drug_order_item
WHERE order_id IN (
    SELECT order_id FROM "Order"
    WHERE order_date <= CURRENT_DATE - INTERVAL '14 days'
);

DELETE FROM Equipment_order_item
WHERE order_id IN (
    SELECT order_id FROM "Order"
    WHERE order_date <= CURRENT_DATE - INTERVAL '14 days'
);

DELETE FROM "Order"
WHERE order_date <= CURRENT_DATE - INTERVAL '14 days';
