-- Insert sample data into Department
INSERT INTO Department (Department_Id, Name, Emergency_level) VALUES (1, 'Emergency', 5);
INSERT INTO Department (Department_Id, Name, Emergency_level) VALUES (2, 'Pediatrics', 3);
INSERT INTO Department (Department_Id, Name, Emergency_level) VALUES (3, 'Radiology', 2);

-- Insert sample data into Logistic_worker
INSERT INTO Logistic_worker (Logistic_worker_Id, Shift_hours, Name) VALUES (101, 8, 'Alice');
INSERT INTO Logistic_worker (Logistic_worker_Id, Shift_hours, Name) VALUES (102, 6, 'Bob');
INSERT INTO Logistic_worker (Logistic_worker_Id, Shift_hours, Name) VALUES (103, 12, 'Charlie');

-- Insert sample data into Warehouse
INSERT INTO Warehouse (Warehouse_Id, Name, Location, Active_hours) VALUES (1, 'Equipment Storage A', 'Building A', '08:00-18:00');
INSERT INTO Warehouse (Warehouse_Id, Name, Location, Active_hours) VALUES (2, 'Equipment Storage B', 'Building B', '09:00-17:00');
INSERT INTO Warehouse (Warehouse_Id, Name, Location, Active_hours) VALUES (3, 'Equipment Storage C', 'Building C', '07:00-15:00');
INSERT INTO Warehouse (Warehouse_Id, Name, Location, Active_hours) VALUES (4, 'Drug Storage A', 'Building D', '24/7');
INSERT INTO Warehouse (Warehouse_Id, Name, Location, Active_hours) VALUES (5, 'Drug Storage B', 'Building E', '24/7');
INSERT INTO Warehouse (Warehouse_Id, Name, Location, Active_hours) VALUES (6, 'Drug Storage C', 'Building F', '24/7');

-- Insert into Medical_Equipment
INSERT INTO Medical_Equipment (Medical_Equipment_Id, Name, Emergency_use, Device_category, Requires_building, Volume)
VALUES (1001, 'MRI Machine', TRUE, 'Imaging', TRUE, 20.50);
INSERT INTO Medical_Equipment (Medical_Equipment_Id, Name, Emergency_use, Device_category, Requires_building, Volume)
VALUES (1002, 'Ventilator', TRUE, 'Respiratory', FALSE, 1.20);
INSERT INTO Medical_Equipment (Medical_Equipment_Id, Name, Emergency_use, Device_category, Requires_building, Volume)
VALUES (1003, 'Infusion Pump', FALSE, 'IV', FALSE, 0.30);

-- Insert into Drug
INSERT INTO Drug (Drug_Id, Name, Shelf_life, Is_frozen, Popularity_score) VALUES (2001, 'Paracetamol', 365, FALSE, 4.75);
INSERT INTO Drug (Drug_Id, Name, Shelf_life, Is_frozen, Popularity_score) VALUES (2002, 'Amoxicillin', 180, FALSE, 4.20);
INSERT INTO Drug (Drug_Id, Name, Shelf_life, Is_frozen, Popularity_score) VALUES (2003, 'Insulin', 90, TRUE, 4.90);

-- Insert into Order (for Department_Id = 1)
INSERT INTO "Order" (Order_Id, Department_Id, Order_Date) VALUES (1, 1, '2025-04-01');
INSERT INTO "Order" (Order_Id, Department_Id, Order_Date) VALUES (2, 1, '2025-04-02');
INSERT INTO "Order" (Order_Id, Department_Id, Order_Date) VALUES (3, 1, '2025-04-03');

-- Insert into Equipment_order_item
INSERT INTO Equipment_order_item (Medical_Equipment_Id, Order_Id, Department_Id, Is_urgent, Amount, Need_to_be_built, Status)
VALUES (1001, 1, 1, TRUE, 1, TRUE, 'Pending');
INSERT INTO Equipment_order_item (Medical_Equipment_Id, Order_Id, Department_Id, Is_urgent, Amount, Need_to_be_built, Status)
VALUES (1002, 2, 1, FALSE, 3, FALSE, 'Approved');
INSERT INTO Equipment_order_item (Medical_Equipment_Id, Order_Id, Department_Id, Is_urgent, Amount, Need_to_be_built, Status)
VALUES (1003, 3, 1, TRUE, 2, FALSE, 'Delivered');

-- Insert into Drug_order_item
INSERT INTO Drug_order_item (Order_Id, Department_Id, Drug_Id, Amount, Is_urgent, Status)
VALUES (1, 1, 2001, 10, TRUE, 'Pending');
INSERT INTO Drug_order_item (Order_Id, Department_Id, Drug_Id, Amount, Is_urgent, Status)
VALUES (2, 1, 2002, 5, FALSE, 'Approved');
INSERT INTO Drug_order_item (Order_Id, Department_Id, Drug_Id, Amount, Is_urgent, Status)
VALUES (3, 1, 2003, 2, TRUE, 'Delivered');

-- Insert into Medical_equipment_warehouse (IDs 1–3)
INSERT INTO Medical_equipment_warehouse (Warehouse_Id, Storage_place, Stock_period)
VALUES (1, 100.50, 60);
INSERT INTO Medical_equipment_warehouse (Warehouse_Id, Storage_place, Stock_period)
VALUES (2, 50.00, 30);
INSERT INTO Medical_equipment_warehouse (Warehouse_Id, Storage_place, Stock_period)
VALUES (3, 25.75, 15);

-- Insert into Drugs_warehouse (IDs 4–6)
INSERT INTO Drugs_warehouse (Warehouse_Id, Has_frozen_area, Daily_drug_audit_time)
VALUES (4, TRUE, '08:00:00');
INSERT INTO Drugs_warehouse (Warehouse_Id, Has_frozen_area, Daily_drug_audit_time)
VALUES (5, FALSE, '09:00:00');
INSERT INTO Drugs_warehouse (Warehouse_Id, Has_frozen_area, Daily_drug_audit_time)
VALUES (6, TRUE, '10:00:00');

-- Insert into Equipment_in_stock (matching Equipment warehouses 1–3)
INSERT INTO Equipment_in_stock (Medical_Equipment_Id, Warehouse_Id, Amount)
VALUES (1001, 1, 2);
INSERT INTO Equipment_in_stock (Medical_Equipment_Id, Warehouse_Id, Amount)
VALUES (1002, 2, 5);
INSERT INTO Equipment_in_stock (Medical_Equipment_Id, Warehouse_Id, Amount)
VALUES (1003, 3, 1);

-- Insert into Drug_in_stock (matching Drug warehouses 4–6)
INSERT INTO Drug_in_stock (Drug_Id, Warehouse_Id, Since, Amount)
VALUES (2001, 4, '2025-03-01', 100);
INSERT INTO Drug_in_stock (Drug_Id, Warehouse_Id, Since, Amount)
VALUES (2002, 5, '2025-03-05', 50);
INSERT INTO Drug_in_stock (Drug_Id, Warehouse_Id, Since, Amount)
VALUES (2003, 6, '2025-03-10', 25);

-- Insert into Works_for
INSERT INTO Works_for (Logistic_worker_Id, Department_Id, Hours)
VALUES (101, 1, 8);
INSERT INTO Works_for (Logistic_worker_Id, Department_Id, Hours)
VALUES (102, 2, 6);
INSERT INTO Works_for (Logistic_worker_Id, Department_Id, Hours)
VALUES (103, 3, 10);

-- Insert into Has_access
INSERT INTO Has_access (Logistic_worker_Id, Warehouse_Id, Level)
VALUES (101, 1, 5);
INSERT INTO Has_access (Logistic_worker_Id, Warehouse_Id, Level)
VALUES (102, 4, 3);
INSERT INTO Has_access (Logistic_worker_Id, Warehouse_Id, Level)
VALUES (103, 6, 4);
