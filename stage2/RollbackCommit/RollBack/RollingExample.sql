BEGIN;

UPDATE Drug
SET popularity_score = 3.33
WHERE drug_id = 1;

SELECT * FROM Drug WHERE drug_id = 1;

ROLLBACK;

SELECT * FROM Drug WHERE drug_id = 1;
