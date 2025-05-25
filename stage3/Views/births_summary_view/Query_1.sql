SELECT 
    d.birth_specialty,
    doctor_name,
    COUNT(*) AS total_births,
    ROUND(AVG(mother_age)::numeric, 1) AS avg_mother_age
FROM 
    births_summary_view d
GROUP BY 
    d.birth_specialty, doctor_name
ORDER BY 
    d.birth_specialty, total_births DESC;
