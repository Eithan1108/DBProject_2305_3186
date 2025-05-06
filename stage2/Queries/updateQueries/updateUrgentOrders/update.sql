UPDATE Drug_order_item
SET status = 'approved'
WHERE is_urgent = TRUE
  AND status IN ('pending', 'waiting')
  AND department_id IN (
      SELECT department_id FROM Department WHERE emergency_level >= 4
  );