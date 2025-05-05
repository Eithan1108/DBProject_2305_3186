-- Drop existing tables if they exist (in correct order to avoid FK issues)
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

-- Department
CREATE TABLE Department (
    Department_Id INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Emergency_level INT CHECK (Emergency_level BETWEEN 1 AND 5)
);

-- Order (weak entity: identified by Department_Id + Order_Id)
CREATE TABLE "Order" (
    Order_Id INT NOT NULL,
    Department_Id INT NOT NULL,
    Order_Date DATE NOT NULL,
    PRIMARY KEY (Department_Id, Order_Id),
    FOREIGN KEY (Department_Id) REFERENCES Department(Department_Id) ON DELETE CASCADE
);

-- Medical Equipment
CREATE TABLE Medical_Equipment (
    Medical_Equipment_Id INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Emergency_use BOOLEAN NOT NULL,
    Device_category VARCHAR(50) NOT NULL,
    Requires_building BOOLEAN NOT NULL,
    Volume DECIMAL(10,2) CHECK (Volume >= 0)
);

-- Drug
CREATE TABLE Drug (
    Drug_Id INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Shelf_life INT CHECK (Shelf_life >= 0),
    Is_frozen BOOLEAN NOT NULL,
    Popularity_score DECIMAL(3,2) CHECK (Popularity_score >= 0 AND Popularity_score <= 5)
);

-- Equipment_order_item (weak entity)
CREATE TABLE Equipment_order_item (
    Medical_Equipment_Id INT NOT NULL,
    Order_Id INT NOT NULL,
    Department_Id INT NOT NULL,
    Is_urgent BOOLEAN NOT NULL,
    Amount INT CHECK (Amount > 0),
    Need_to_be_built BOOLEAN NOT NULL,
    Status VARCHAR(50) NOT NULL,
    PRIMARY KEY (Medical_Equipment_Id, Order_Id, Department_Id),
    FOREIGN KEY (Medical_Equipment_Id) REFERENCES Medical_Equipment(Medical_Equipment_Id) ON DELETE CASCADE,
    FOREIGN KEY (Order_Id, Department_Id) REFERENCES "Order"(Order_Id, Department_Id) ON DELETE CASCADE
);

-- Drug_order_item (weak entity)
CREATE TABLE Drug_order_item (
    Order_Id INT NOT NULL,
    Department_Id INT NOT NULL,
    Drug_Id INT NOT NULL,
    Amount INT CHECK (Amount > 0),
    Is_urgent BOOLEAN NOT NULL,
    Status VARCHAR(50) NOT NULL,
    PRIMARY KEY (Order_Id, Department_Id, Drug_Id),
    FOREIGN KEY (Order_Id, Department_Id) REFERENCES "Order"(Order_Id, Department_Id) ON DELETE CASCADE,
    FOREIGN KEY (Drug_Id) REFERENCES Drug(Drug_Id) ON DELETE CASCADE
);

-- Warehouse
CREATE TABLE Warehouse (
    Warehouse_Id INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    Active_hours VARCHAR(50)
);

-- Medical_equipment_warehouse (inherits Warehouse)
CREATE TABLE Medical_equipment_warehouse (
    Warehouse_Id INT PRIMARY KEY,
    Storage_place DECIMAL(10,2) CHECK (Storage_place >= 0),
    Stock_period INT CHECK (Stock_period >= 0),
    FOREIGN KEY (Warehouse_Id) REFERENCES Warehouse(Warehouse_Id) ON DELETE CASCADE
);

-- Drugs_warehouse (inherits Warehouse)
CREATE TABLE Drugs_warehouse (
    Warehouse_Id INT PRIMARY KEY,
    Has_frozen_area BOOLEAN NOT NULL,
    Daily_drug_audit_time TIME NOT NULL,
    FOREIGN KEY (Warehouse_Id) REFERENCES Warehouse(Warehouse_Id) ON DELETE CASCADE
);

-- Equipment_in_stock
CREATE TABLE Equipment_in_stock (
    Medical_Equipment_Id INT NOT NULL,
    Warehouse_Id INT NOT NULL,
    Amount INT CHECK (Amount >= 0),
    PRIMARY KEY (Medical_Equipment_Id, Warehouse_Id),
    FOREIGN KEY (Medical_Equipment_Id) REFERENCES Medical_Equipment(Medical_Equipment_Id) ON DELETE CASCADE,
    FOREIGN KEY (Warehouse_Id) REFERENCES Warehouse(Warehouse_Id) ON DELETE CASCADE
);

-- Drug_in_stock
CREATE TABLE Drug_in_stock (
    Drug_Id INT NOT NULL,
    Warehouse_Id INT NOT NULL,
    Since DATE NOT NULL,
    Amount INT CHECK (Amount >= 0),
    PRIMARY KEY (Drug_Id, Warehouse_Id, Since),
    FOREIGN KEY (Drug_Id) REFERENCES Drug(Drug_Id) ON DELETE CASCADE,
    FOREIGN KEY (Warehouse_Id) REFERENCES Warehouse(Warehouse_Id) ON DELETE CASCADE
);

-- Logistic_worker
CREATE TABLE Logistic_worker (
    Logistic_worker_Id INT PRIMARY KEY,
    Shift_hours INT CHECK (Shift_hours > 0),
    Name VARCHAR(100) NOT NULL
);

-- Works_for (many-to-many between workers and departments)
CREATE TABLE Works_for (
    Logistic_worker_Id INT NOT NULL,
    Department_Id INT NOT NULL,
    Hours INT CHECK (Hours >= 0),
    PRIMARY KEY (Logistic_worker_Id, Department_Id),
    FOREIGN KEY (Logistic_worker_Id) REFERENCES Logistic_worker(Logistic_worker_Id) ON DELETE CASCADE,
    FOREIGN KEY (Department_Id) REFERENCES Department(Department_Id) ON DELETE CASCADE
);

-- Has_access (many-to-many between workers and warehouses)
CREATE TABLE Has_access (
    Logistic_worker_Id INT NOT NULL,
    Warehouse_Id INT NOT NULL,
    Level INT CHECK (Level BETWEEN 1 AND 5),
    PRIMARY KEY (Logistic_worker_Id, Warehouse_Id),
    FOREIGN KEY (Logistic_worker_Id) REFERENCES Logistic_worker(Logistic_worker_Id) ON DELETE CASCADE,
    FOREIGN KEY (Warehouse_Id) REFERENCES Warehouse(Warehouse_Id) ON DELETE CASCADE
);
