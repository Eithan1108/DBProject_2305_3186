# Hospital Medical Equipment Logistics System

## Overview
This project implements a comprehensive PostgreSQL database system for managing hospital logistics operations, with a specific focus on medical equipment and supplies. The system tracks the flow of medical equipment and drugs between departments and warehouses, manages orders, monitors inventory levels, and coordinates logistics personnel activities.

## Table of Contents
- [Database Structure](#database-structure)
- [Entity Relationship Diagram](#entity-relationship-diagram)
- [Setup Instructions](#setup-instructions)
- [Data Population](#data-population)
- [Backup and Restore](#backup-and-restore)
- [Project Structure](#project-structure)
- [Project Phases](#project-phases)

## Database Structure

The database consists of 14 interconnected tables that model the following entities:

1. **Department** - Hospital departments that place orders for medical supplies
2. **Order** - Department requests for medical equipment and drugs
3. **Medical Equipment** - Information about available medical devices and their specifications
4. **Drug** - Pharmaceutical products stocked and ordered by departments
5. **Equipment_order_item** - Details of equipment items in department orders
6. **Drug_order_item** - Details of drug items in department orders
7. **Warehouse** - Storage facilities for medical supplies and equipment
8. **Medical_equipment_warehouse** - Specialized warehouses for medical equipment
9. **Drugs_warehouse** - Specialized warehouses for pharmaceutical products
10. **Equipment_in_stock** - Inventory tracking of equipment in warehouses
11. **Drug_in_stock** - Inventory tracking of drugs in warehouses
12. **Logistic_worker** - Personnel responsible for managing logistics operations
13. **Works_for** - Relationship between logistics workers and departments
14. **Has_access** - Access permissions for logistics workers to warehouses

Each entity contains multiple attributes that describe various aspects of the hospital logistics system, with appropriate relationships established between entities to maintain data integrity and functionality.

## Entity Relationship Diagram

The system is designed according to the following Entity-Relationship model:

![ER Diagram](ERD_diagram.png)

*Note: The ER diagram is included in the repository and visualizes the relationships between all entities in the database system.*

## Setup Instructions

### Prerequisites
- PostgreSQL 14.0 or higher
- psql command-line tool or pgAdmin 4

### Database Creation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hospital-logistics-db.git
cd hospital-logistics-db
```

2. Connect to PostgreSQL:
```bash
psql -U postgres
```

3. Create a new database:
```sql
CREATE DATABASE hospital_logistics;
\c hospital_logistics
```

4. Run the table creation script:
```bash
psql -U postgres -d hospital_logistics -f createTables.sql
```

## Data Population

The database is populated with realistic test data using three different methods:

1. **Mockaroo Data Generation** - Utilizing Mockaroo to generate structured random data
2. **Python Script Generation** - Custom Python scripts to create test data with appropriate relationships
3. **CSV/Excel Imports** - Data imported from prepared spreadsheets

Each table contains at least 400 records to enable meaningful query testing and analysis.

### Sample Data Loading

To load the sample data into your database:

```bash
psql -U postgres -d hospital_logistics -f insertTables.sql
```

## Backup and Restore

The database is backed up regularly using PostgreSQL's built-in utilities.

### Creating a Backup
```bash
pg_dump -U postgres hospital_logistics > backup_YYYYMMDD.sql
```

### Restoring from Backup
```bash
psql -U postgres -d hospital_logistics -f backup_YYYYMMDD.sql
```

The backup process has been tested on separate systems to ensure data integrity and recoverability.

## Project Structure

The repository is organized as follows:

```
DBProject/
├── שלב א/
│   ├── ERD.png
│   ├── DSD.png
│   ├── createTables.sql
│   ├── dropTables.sql
│   ├── insertTables.sql
│   ├── selectAll.sql
│   ├── DataImportFiles/
│   │   └── [CSV and configuration files]
│   ├── Programming/
│   │   └── [Python scripts for data generation]
│   ├── mockarooFiles/
│   │   └── [Mockaroo-generated SQL files]
│   └── backup_YYYYMMDD.sql
├── README.md
└── [Additional project phase directories]
```

## Project Phases

The project is divided into five phases:

1. **Database Design and Data Population** - Creating the database schema, ERD design, and populating with test data
2. **Query Development** - Creating complex queries to extract meaningful information
3. **Integration and Views** - Developing database views and integration points
4. **PL/pgSQL Programming** - Creating stored procedures and functions
5. **Graphical Interface** - Developing a user interface for the system

Each phase builds upon the previous work, resulting in a fully functional hospital logistics management system.
