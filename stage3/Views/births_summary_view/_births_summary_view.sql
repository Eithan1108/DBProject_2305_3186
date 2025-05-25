 SELECT br.id_br,
    m.name AS mother_name,
    m.age AS mother_age,
    m.phone AS mother_phone,
    br.birth_date,
    br.discharge_date,
    br.delivery_type,
    d.name AS doctor_name,
    d.birth_specialty,
    d.seniority
   FROM birth_record br
     JOIN maternity m ON br.id_m = m.id_m
     JOIN midwife mw ON br.id_br = mw.id_br
     JOIN doctor d ON mw.id_d = d.id_d;