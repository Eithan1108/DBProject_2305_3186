SELECT 
    doctor_name,
    seniority,
    mother_name,
    birth_date,
    discharge_date
FROM 
    births_summary_view
WHERE 
    delivery_type = 'Vaginal'
    AND birth_date >= CURRENT_DATE - INTERVAL '6 months'
    AND birth_date <= CURRENT_DATE
    AND seniority >= 10
ORDER BY 
    birth_date DESC;
