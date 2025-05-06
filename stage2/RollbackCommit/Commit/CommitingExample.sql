BEGIN;

UPDATE Drug
SET popularity_score = 4.78
WHERE drug_id = 1;

SELECT * FROM Drug WHERE drug_id = 1;

COMMIT;

SELECT * FROM Drug WHERE drug_id = 1;
