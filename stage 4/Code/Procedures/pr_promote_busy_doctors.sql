CREATE OR REPLACE PROCEDURE pr_promote_busy_doctors()
LANGUAGE plpgsql AS $$
DECLARE
    dep_id INTEGER;
    rec RECORD;
BEGIN
    FOR dep_id IN SELECT DISTINCT department_id FROM maternity LOOP
        FOR rec IN SELECT * FROM fn_get_top5_doctors(dep_id) LOOP
            UPDATE doctor
               SET seniority = seniority + 1
             WHERE id_d = rec.id_d;
        END LOOP;
    END LOOP;
END;
$$;