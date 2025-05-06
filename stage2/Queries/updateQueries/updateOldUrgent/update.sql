UPDATE Drug_order_item
SET status = 'approved'
WHERE is_urgent = TRUE
  AND status IN ('pending', 'waiting')
  AND order_id IN (
      SELECT order_id
      FROM "Order"
      WHERE order_date <= CURRENT_DATE - INTERVAL '3 days'
  );
