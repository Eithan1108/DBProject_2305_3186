ALTER TABLE Drug_in_stock
ADD CONSTRAINT chk_since
CHECK (since <= CURRENT_DATE );

ALTER TABLE Drug_order_item
ADD CONSTRAINT chk_drug_order_item_positive_amount
CHECK (amount > 0);

ALTER TABLE Equipment_order_item
ADD CONSTRAINT chk_equipment_order_item_positive_amount
CHECK (amount > 0);

ALTER TABLE Drug_order_item
ALTER COLUMN is_urgent SET DEFAULT FALSE;

ALTER TABLE Equipment_order_item
ALTER COLUMN is_urgent SET DEFAULT FALSE;

ALTER TABLE Drug_in_stock
ALTER COLUMN since SET NOT NULL;
