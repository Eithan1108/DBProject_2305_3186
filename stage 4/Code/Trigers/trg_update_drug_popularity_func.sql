CREATE OR REPLACE FUNCTION trg_update_drug_popularity_func()
RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        CALL pr_refresh_drug_popularity(NEW.drug_id);
    ELSE
        CALL pr_refresh_drug_popularity(OLD.drug_id);
    END IF;
    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_update_drug_popularity
AFTER INSERT OR DELETE ON drug_order_item
FOR EACH ROW
EXECUTE FUNCTION trg_update_drug_popularity_func();