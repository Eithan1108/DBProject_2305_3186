CREATE OR REPLACE FUNCTION fn_popular_score(p_drug_id integer)
RETURNS numeric
LANGUAGE plpgsql AS $$
DECLARE
    v_drug_orders  bigint;
    v_total_orders bigint;
BEGIN
    SELECT COUNT(DISTINCT order_id)
      INTO v_drug_orders
      FROM drug_order_item
     WHERE drug_id = p_drug_id;

    SELECT COUNT(*) INTO v_total_orders FROM "Order";

    IF v_total_orders = 0 THEN
        RETURN 0;
    END IF;

    RETURN ROUND(v_drug_orders::numeric * 100 / v_total_orders, 2);
END;
$$;