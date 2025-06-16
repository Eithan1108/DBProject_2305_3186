CREATE OR REPLACE FUNCTION fn_get_top5_doctors(p_department_id integer)
RETURNS TABLE(id_d integer, name character varying, births bigint)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
        SELECT d.id_d,
               d.name,
               COUNT(*) AS births
          FROM midwife       mw
          JOIN doctor        d  ON d.id_d = mw.id_d
          JOIN birth_record  br ON br.id_br = mw.id_br
          JOIN maternity     m  ON m.id_m  = br.id_m
         WHERE m.department_id = p_department_id
         GROUP BY d.id_d, d.name
         ORDER BY births DESC
         LIMIT 5;
END;
$$;