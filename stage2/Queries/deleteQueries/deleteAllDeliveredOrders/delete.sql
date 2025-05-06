DELETE FROM Drug_order_item
WHERE order_id IN (
    SELECT order_id FROM "Order"
    WHERE NOT EXISTS (
        SELECT 1 FROM Drug_order_item d
        WHERE d.order_id = "Order".order_id
          AND d.status NOT IN ('delivered')
    )
    AND NOT EXISTS (
        SELECT 1 FROM Equipment_order_item e
        WHERE e.order_id = "Order".order_id
          AND e.status NOT IN ('delivered')
    )
);

DELETE FROM Equipment_order_item
WHERE order_id IN (
    SELECT order_id FROM "Order"
    WHERE NOT EXISTS (
        SELECT 1 FROM Drug_order_item d
        WHERE d.order_id = "Order".order_id
          AND d.status NOT IN ('delivered')
    )
    AND NOT EXISTS (
        SELECT 1 FROM Equipment_order_item e
        WHERE e.order_id = "Order".order_id
          AND e.status NOT IN ('delivered')
    )
);

DELETE FROM "Order"
WHERE order_id IN (
    SELECT order_id FROM "Order"
    WHERE NOT EXISTS (
        SELECT 1 FROM Drug_order_item d
        WHERE d.order_id = "Order".order_id
          AND d.status NOT IN ('delivered')
    )
    AND NOT EXISTS (
        SELECT 1 FROM Equipment_order_item e
        WHERE e.order_id = "Order".order_id
          AND e.status NOT IN ('delivered')
    )
);
