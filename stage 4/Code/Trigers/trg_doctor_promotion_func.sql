CREATE OR REPLACE FUNCTION trg_doctor_promotion_func()
RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    CALL pr_promote_busy_doctors();
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_doctor_promotion
AFTER INSERT ON midwife
FOR EACH ROW
EXECUTE FUNCTION trg_doctor_promotion_func();