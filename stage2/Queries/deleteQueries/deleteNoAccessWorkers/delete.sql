DELETE FROM Logistic_worker
WHERE logistic_worker_id NOT IN (
    SELECT DISTINCT logistic_worker_id FROM Has_access
);