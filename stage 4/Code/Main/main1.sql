DO $$
DECLARE
    rec record;
BEGIN
    RAISE NOTICE '--- Top-5 BEFORE promotion ---';
    FOR rec IN SELECT * FROM fn_get_top5_doctors(341) LOOP
        RAISE NOTICE '% - % births (seniority=%)',
                     rec.name, rec.births,
                     (SELECT seniority FROM doctor WHERE id_d = rec.id_d);
    END LOOP;

    CALL pr_promote_busy_doctors();  -- פרוצדורה שמקדמת רק את הטופ 5

    RAISE NOTICE '--- Top-5 AFTER promotion ---';
    FOR rec IN SELECT * FROM fn_get_top5_doctors(341) LOOP
        RAISE NOTICE '% - % births (seniority=%)',
                     rec.name, rec.births,
                     (SELECT seniority FROM doctor WHERE id_d = rec.id_d);
    END LOOP;
END;
$$ LANGUAGE plpgsql;