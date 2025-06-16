CREATE OR REPLACE PROCEDURE pr_refresh_drug_popularity(p_drug_id integer DEFAULT NULL)
LANGUAGE plpgsql AS $$
DECLARE
    rec     record;
    v_score numeric;
BEGIN
    IF p_drug_id IS NOT NULL THEN
        v_score := fn_popular_score(p_drug_id);
        UPDATE drug
           SET popularity_score = v_score
         WHERE drug_id = p_drug_id;
    ELSE
        FOR rec IN SELECT drug_id FROM drug LOOP
            v_score := fn_popular_score(rec.drug_id);
            UPDATE drug
               SET popularity_score = v_score
             WHERE drug_id = rec.drug_id;
        END LOOP;
    END IF;
END;
$$;