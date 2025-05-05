UPDATE Drug_in_stock
SET amount = amount * 2
WHERE drug_id IN (
    SELECT drug_id
    FROM Drug
    WHERE popularity_score > 4.5
);
