CREATE TABLE maternity_department (
    department_id INT PRIMARY KEY REFERENCES department(department_id) ON DELETE CASCADE,
    delivery_types_supported TEXT[],
    birth_support_level TEXT
);

INSERT INTO maternity_department (department_id, delivery_types_supported, birth_support_level) VALUES
(396, ARRAY['natural', 'epidural', 'c-section'], 'intermediate'),
(390, ARRAY['natural', 'epidural', 'c-section', 'VBAC', 'induced'], 'full'),
(341, ARRAY['natural', 'c-section'], 'basic');


ALTER TABLE room
    ADD COLUMN IF NOT EXISTS department_id integer;




UPDATE room
SET    department_id = 341
WHERE  department_id IS NULL;



ALTER TABLE room
    ALTER COLUMN department_id SET NOT NULL;



ALTER TABLE maternity      DROP CONSTRAINT IF EXISTS maternity_id_r_fkey;
ALTER TABLE attending_to   DROP CONSTRAINT IF EXISTS attending_to_id_r_fkey;
ALTER TABLE room           DROP CONSTRAINT IF EXISTS room_pkey;


ALTER TABLE room
    ADD CONSTRAINT room_pkey PRIMARY KEY (id_r, department_id);




ALTER TABLE room
    ADD CONSTRAINT room_department_fk
        FOREIGN KEY (department_id)
        REFERENCES maternity_department (department_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE;




ALTER TABLE maternity
    ADD COLUMN IF NOT EXISTS department_id integer;



UPDATE maternity m
SET    department_id = r.department_id
FROM   room r
WHERE  m.id_r = r.id_r
  AND  m.department_id IS NULL;



ALTER TABLE maternity
    ALTER COLUMN department_id SET NOT NULL;



ALTER TABLE maternity
    ADD CONSTRAINT maternity_room_fk
        FOREIGN KEY (id_r, department_id)
        REFERENCES room (id_r, department_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT;




ALTER TABLE attending_to
    ADD COLUMN IF NOT EXISTS department_id integer;

UPDATE attending_to a
SET    department_id = r.department_id
FROM   room r
WHERE  a.id_r = r.id_r
  AND  a.department_id IS NULL;

ALTER TABLE attending_to
    ALTER COLUMN department_id SET NOT NULL;



ALTER TABLE attending_to DROP CONSTRAINT IF EXISTS attending_to_pkey;

ALTER TABLE attending_to
    ADD CONSTRAINT attending_to_pkey
        PRIMARY KEY (id_r, department_id, id_n);

ALTER TABLE attending_to
    ADD CONSTRAINT attending_to_room_fk
        FOREIGN KEY (id_r, department_id)
        REFERENCES room (id_r, department_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT;








