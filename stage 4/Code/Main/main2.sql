DO $$
DECLARE
    v_score numeric;
BEGIN
    -- פונקציה on-the-fly – מחשבת בלי להסתמך על הטבלה
    RAISE NOTICE 'AFTER  fn_popular_score = %', fn_popular_score(5555);

    -- ריענון ידני (למרות שהטריגר כבר עשה זאת)
    CALL pr_refresh_drug_popularity(5555);

    -- בדיקה שהערך בטבלה זהה למה שחישבנו
    SELECT popularity_score INTO v_score
      FROM drug WHERE drug_id = 5555;
    RAISE NOTICE 'AFTER  popularity_score column = %', v_score;
END;
$$ LANGUAGE plpgsql;