-- Drop all tables in reverse dependency order to avoid foreign key conflicts
DROP TABLE IF EXISTS Has_access;
DROP TABLE IF EXISTS Works_for;
DROP TABLE IF EXISTS Drug_in_stock;
DROP TABLE IF EXISTS Equipment_in_stock;
DROP TABLE IF EXISTS Drugs_warehouse;
DROP TABLE IF EXISTS Medical_equipment_warehouse;
DROP TABLE IF EXISTS Drug_order_item;
DROP TABLE IF EXISTS Equipment_order_item;
DROP TABLE IF EXISTS Drug;
DROP TABLE IF EXISTS Medical_Equipment;
DROP TABLE IF EXISTS "Order";
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Warehouse;
DROP TABLE IF EXISTS Logistic_worker;