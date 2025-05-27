# Hospital Medical Equipment Logistics System

## Submitted by:
- **Student Name 1:** Hananel Kidron ID: 214262305
- **Student Name 2:** Eitan Klein ID: 215013186

**System**: Hospital Management System  
**Selected Unit**: Medical Equipment Logistics Division

## Overview
This project implements a comprehensive PostgreSQL database system for managing hospital logistics operations, with a specific focus on medical equipment and supplies. The system tracks the flow of medical equipment and drugs between departments and warehouses, manages orders, monitors inventory levels, and coordinates logistics personnel activities.

## Table of Contents
- [Database Structure](#database-structure)
- [Entity Relationship Diagram](#entity-relationship-diagram)
- [Entity and Relationship Overview](#entity-and-relationship-overview)
- [Data Population Methods](#data-population-methods)
- [Backup and Restore](#backup-and-restore)
- [Project Structure](#project-structure)
- [Project Phases](#project-phases)

## Database Structure

The database consists of 14 interconnected tables that model the following entities:

1. **Department** - Hospital departments that place orders for medical supplies
2. **Order** - Department requests for medical equipment and drugs
3. **Medical Equipment** - Comprehensive catalog of all medical devices and their specifications, regardless of current inventory status
4. **Drug** - Complete database of all pharmaceutical products that could be ordered by departments, including those not currently in stock
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

## Entity and Relationship Overview

### Warehouse
There are two specialized types of warehouses in the system: **Drug Warehouses** and **Equipment Warehouses**, both inheriting from the base `Warehouse` entity.  
Each type includes attributes relevant to its function, such as cooling capacity, physical dimensions, and daily audit schedules.

### Drug
Represents a single type of drug (not individual units).  
Each drug type can exist in multiple warehouses, in unlimited quantities.  
Within a warehouse, different batches of the same drug are distinguished by the `since` attribute (entry date), allowing for expiration management and FIFO stock handling.

### Medical_Equipment
Represents a single type of medical equipment.  
Like drugs, each equipment type can be stored in multiple warehouses in unlimited quantities.  
There is no differentiation by entry date—only by type and amount.

### Department
Each department in the hospital can submit orders for drugs or equipment.  
Orders cannot exist independently and must be associated with a department.  
This makes `Order` a **weak entity**, fully dependent on the existence of a `Department`.

### Order
An order may include both drug items and equipment items.  
Each order item is uniquely identified by a combination of:
- `Order ID`
- `Department ID`
- `Drug ID` or `Equipment ID`  
This ensures proper tracking of each specific item within a given order.

### Logistic_Worker
A logistic worker may be assigned to multiple departments, and each department may have multiple workers.  
This many-to-many relationship is managed via the `Works_for` table, which includes the number of hours worked in each department.

### Has_Access
This table manages access rights between logistic workers and warehouses.  
Each warehouse can have multiple workers with access, and each worker can access multiple warehouses.  
An optional `level` attribute can represent the level of access or permissions granted.




## Entity Relationship Diagram

The system is designed according to the following Entity-Relationship models:

### Entity Relationship Diagram (ERD)
![ER Diagram](./stage1/ERD_DSD/ERD.jpg)

### Data Structure Diagram (DSD)
![DS Diagram](./stage1/ERD_DSD/DSD.jpg)

*Note: These diagrams visualize the relationships between all entities in the database system and were created using ERDPlus.*

## Data Population Methods

The database has been populated using three different data insertion methods as required:

### 1. Mockaroo Data Generation

We used Mockaroo to generate structured random data for several tables, including:

#### Drug Table
![Drug Mockaroo Build](./stage1/Data/mockaroo/drug/drug_mockaroo_build.jpg)
![Drug Upload Screenshot](./stage1/Data/mockaroo/drug/drug_upload_screen_shot.jpg)
![Database Upload Successful](./stage1/Data/mockaroo/drug/general_worked.jpg)

#### Logistic Worker Table
![Logistic Worker Mockaroo Build](./stage1/Data/mockaroo/logistic_worker/logistic_worker_mockaroo_build.jpg)
![Logistic Worker Upload Screenshot](./stage1/Data/mockaroo/logistic_worker/logistic_worker_upload_screen_shot.jpg)
![Database Upload Successful](./stage1/Data/mockaroo/logistic_worker/general_worked.jpg)

### 2. CSV Import

We imported data directly from prepared CSV files for tables such as Has_access:
![Has Access CSV Upload](./stage1/Data/csv_upload/has_access_upload_screen_shot.jpg)
![Has Access Upload Successful](./stage1/Data/csv_upload/has_access_upload_screen_shot_worked.jpg)

### 3. Python Scripts

We created custom Python scripts to generate data for multiple tables. Our scripts ensure proper relationships between entities and generate the required volume of data (at least 400 records per table).

Python scripts were created for the following tables:
- Department
- Order
- Drug_in_stock
- Drug_order_item
- Equipment_in_stock
- Equipment_order_item
- Medical_equipment
- Medical_equipment_warehouse
- Warehouse
- Works_for
- Drugs_warehouse

## Backup and Restore

### Database Backup

We performed database backup using PostgreSQL's built-in utilities to ensure data preservation.

![Backup Operation Screenshot](./stage1/Backup/Screenshot_of_the_backup_operation.jpg)

### Database Restoration

We verified the backup integrity by successfully restoring it on a different system:

![Restore Operation Screenshot 1](./stage1/Backup/Screenshot_of_the_restore_operation1.png)
![Restore Operation Screenshot 2](./stage1/Backup/Screenshot_of_the_restore_operation2.png)
![Restore Operation Screenshot 3](./stage1/Backup/Screenshot_of_the_restore_operation3.png)

The backup file `second_backup_02052025` was successfully restored, confirming the validity of our backup process.

## Project Structure

The repository is organized as follows:

```
Project Structure:
│
├── README.md
│
└── stage1/
    ├── Backup/
    │   ├── Screenshot_of_the_backup_operation.jpg
    │   ├── Screenshot_of_the_restore_operation1.png
    │   ├── Screenshot_of_the_restore_operation2.png
    │   ├── Screenshot_of_the_restore_operation3.png
    │   └── second_backup_02052025
    │
    ├── Data/
    │   ├── csv_upload/
    │   │   ├── has_access.csv
    │   │   ├── has_access_upload_screen_shot.jpg
    │   │   └── has_access_upload_screen_shot_worked.jpg
    │   │
    │   ├── mockaroo/
    │   │   ├── drug/
    │   │   │   ├── drug_mockaroo_build.jpg
    │   │   │   ├── drug_upload_screen_shot.jpg
    │   │   │   └── general_worked.jpg
    │   │   │
    │   │   └── logistic_worker/
    │   │       ├── general_worked.jpg
    │   │       ├── logistic_worker_mockaroo_build.jpg
    │   │       └── logistic_worker_upload_screen_shot.jpg
    │   │
    │   └── python_scripts/
    │       ├── Department.py
    │       ├── Drugs_warehouse.py
    │       ├── Drug_in_stock.py
    │       ├── Drug_order_item.py
    │       ├── equipment_in_stock.py
    │       ├── equipment_order_item.py
    │       ├── medical_equipment.py
    │       ├── medical_equipment_warehouse.py
    │       ├── Order.py
    │       ├── warehouse.py
    │       └── works_for.py
    │
    ├── ERD_DSD/
    │   ├── DSD.jpg
    │   └── ERD.jpg
    │
    └── Ganeric_actions/
        ├── createTable.sql
        ├── dropTables.sql
        ├── insertTables.sql
        └── selectAll.sql
```

## Project Phases

The project is divided into five phases:

1. **Database Design and Data Population** - Creating the database schema, ERD design, and populating with test data
2. **Query Development** - Creating complex queries to extract meaningful information
3. **Integration and Views** - Developing database views and integration points
4. **PL/pgSQL Programming** - Creating stored procedures and functions
5. **Graphical Interface** - Developing a user interface for the system

Each phase builds upon the previous work, resulting in a fully functional hospital logistics management system.









# Stage 2: SQL Queries, Constraints, and Transaction Management

The second stage of the Hospital Medical Equipment Logistics System project focuses on implementing advanced SQL features, including complex SELECT queries, data modification operations (UPDATE and DELETE), constraints, and transaction management.

## Table of Contents for Stage 2

- [Project Structure](#project-structure-for-stage-2)
- [SELECT Queries](#select-queries)
- [DELETE Operations](#delete-operations)
- [UPDATE Operations](#update-operations)
- [Constraints](#constraints)
- [Transaction Management (ROLLBACK and COMMIT)](#transaction-management)

## Project Structure for Stage 2

```
stage2/
├── Constraints/
│   ├── Constraints.sql
│   ├── DefaultUrgentDrug.jpg
│   ├── DfaultUrgentEq.jpg
│   ├── DrugAmount0.jpg
│   ├── DrugStockDate.jpg
│   ├── EqAmount0.jpg
│   └── NullSinceDrugStock.jpg
│
├── Queries/
│   ├── deleteAllDelivered Orders/
│   │   ├── After.jpg
│   │   ├── Before.jpg
│   │   ├── delete.sql
│   │   └── Done.jpg
│   │
│   ├── deleteExpiredOrders/
│   │   ├── After.jpg
│   │   ├── Before.jpg
│   │   ├── delete.sql
│   │   └── Done.jpg
│   │
│   ├── deleteNoAccessWorkers/
│   │   ├── After.jpg
│   │   ├── Before.jpg
│   │   ├── delete.sql
│   │   └── Done.jpg
│   │
│   ├── selectQueries/
│   │   ├── Employee access to warehouses/
│   │   │   ├── result.jpg
│   │   │   ├── running.jpg
│   │   │   └── select.sql
│   │   │
│   │   ├── For each item, how many warehouses is it located in/
│   │   │   ├── result.jpg
│   │   │   ├── running.jpg
│   │   │   └── select.sql
│   │   │
│   │   ├── Items to pick by warehouse for a specific employee/
│   │   │   ├── result.jpg
│   │   │   ├── running.jpg
│   │   │   └── select.sql
│   │   │
│   │   ├── lack of stock/
│   │   │   ├── result.jpg
│   │   │   ├── running.png
│   │   │   └── select.sql
│   │   │
│   │   ├── Medicines in danger of expiring/
│   │   │   ├── result.jpg
│   │   │   ├── running.jpg
│   │   │   └── select.sql
│   │   │
│   │   ├── The most needed medications/
│   │   │   ├── result.jpg
│   │   │   ├── runnig.jpg
│   │   │   └── select.sql
│   │   │
│   │   ├── Urgent items for each department/
│   │   │   ├── result.png
│   │   │   ├── running.jpg
│   │   │   └── urgentItems.sql
│   │   │
│   │   └── Warehouse inventory summary/
│   │       ├── result.jpg
│   │       ├── running.jpg
│   │       └── select.sql
│   │
│   ├── updateOldUrgent/
│   │   ├── After.jpg
│   │   ├── Before.jpg
│   │   └── update.sql
│   │
│   ├── updatePopularDrugs/
│   │   ├── After.jpg
│   │   ├── Before.jpg
│   │   ├── Done.jpg
│   │   └── update.sql
│   │
│   └── updateUrgentOrders/
│       ├── After.jpg
│       ├── Before.jpg
│       ├── Done.jpg
│       └── update.sql
│
└── RollbackCommit/
    ├── Commit/
    │   ├── Commiting.jpg
    │   ├── CommitingExample.sql
    │   ├── Update.jpg
    │   └── UpdateSaved.jpg
    │
    └── RollBack/
        ├── AfterRollingBack.jpg
        ├── RollingBack.jpg
        ├── RollingExample.sql
        └── Updated.jpg
```

## SELECT Queries

### 1. Urgent Items for Each Department

**שאילתה זו מציגה את מספר הפריטים הדחופים (תרופות וציוד רפואי) בכל מחלקה. היא מסייעת לניהול המשאבים על ידי זיהוי מחלקות הזקוקות לטיפול מיידי. התוצאות מציגות עבור כל מחלקה את מספר פריטי התרופות הדחופים, מספר פריטי הציוד הדחופים והסכום הכולל, מסודר לפי המחלקות עם המספר הגבוה ביותר של פריטים דחופים.**

![Urgent Items Query Execution Screenshot](./stage2/Queries/selectQueries/Urgentitemsforeachdepartment/running.jpg)

![Urgent Items Query Results](./stage2/Queries/selectQueries/Urgentitemsforeachdepartment/result.png)

### 2. The Most Needed Medications

**שאילתה זו מזהה אילו תרופות נדרשות בתדירות הגבוהה ביותר ובכמויות הגדולות ביותר. מידע זה חיוני לניהול מלאי יעיל ולתכנון רכש. התוצאות מציגות עבור כל תרופה את מספר ההזמנות שבהן היא מופיעה וסך כל הכמות שהוזמנה, מסודר לפי הכמות הכוללת בסדר יורד.**

![Query Execution Screenshot](./stage2/Queries/selectQueries/Themostneededmedications/runnig.jpg)

![Query Results](./stage2/Queries/selectQueries/Themostneededmedications/result.jpg)

### 3. Lack of Stock

**שאילתה זו מזהה פריטים (תרופות וציוד רפואי) שבהם סך כל הכמות המוזמנת בכל ההזמנות יחד גדולה מסך כל הכמות הזמינה במלאי. עבור כל פריט, היא מחשבת את סך כל הכמות המוזמנת מכל המחלקות ומשווה אותה לסך כל המלאי הזמין בכל המחסנים. התוצאות מציגות את שם הפריט, הכמות שהוזמנה, הכמות הזמינה במלאי וגודל המחסור. התוצאות מסודרות לפי גודל המחסור בסדר יורד, מה שמסייע לניהול הרכש להתמקד תחילה בפריטים עם המחסור החמור ביותר.**

![Query Execution Screenshot](./stage2/Queries/selectQueries/lackofstock/running.png)

![Query Results](./stage2/Queries/selectQueries/lackofstock/result.jpg)

### 4. Warehouse Inventory Summary

**שאילתה זו מספקת סקירה מקיפה של המלאי בכל המחסנים. עבור כל מחסן, היא מציגה את מספר סוגי התרופות וסך הכמות שלהן, או את מספר סוגי הציוד הרפואי וסך הכמות שלו. התוצאות מסודרות לפי הכמות הגדולה ביותר של פריטים במחסן (בין אם מדובר בתרופות או ציוד). שאילתה זו מסייעת בניהול המחסנים, במעקב אחר המלאי ובתכנון הרכש, ומספקת תמונה ברורה של היקף המלאי בכל מחסן.**

![Query Execution Screenshot](./stage2/Queries/selectQueries/Warehouseinventorysummary/running.jpg)

![Query Results](./stage2/Queries/selectQueries/Warehouseinventorysummary/result.jpg)

### 5. Employee Access to Warehouses

**שאילתה זו מציגה לאילו מחסנים יש לכל עובד לוגיסטיקה גישה. היא מסייעת בתכנון משמרות ובהקצאת משימות לעובדים. התוצאות מציגות עבור כל עובד את מספר המחסנים שיש לו גישה אליהם ואת שמות המחסנים, מסודר לפי העובדים עם הגישה למספר הרב ביותר של מחסנים.**

![Query Execution Screenshot](./stage2/Queries/selectQueries/Employeeaccesstowarehouses/running.jpg)

![Query Results](./stage2/Queries/selectQueries/Employeeaccesstowarehouses/result.jpg)

### 6. Medicines in Danger of Expiring

**שאילתה זו מזהה תרופות שעלולות לפוג בקרוב. היא מסייעת במניעת בזבוז ומבטיחה שהתרופות ישמשו לפני שיפוגו. התוצאות מציגות תרופות שנותר להן פחות מחודש עד לתפוגה, כולל תאריך הכנסתן למלאי, מספר הימים שעברו מאז, אורך חיי המדף שלהן ומספר הימים שנותרו עד לתפוגה.**

![Query Execution Screenshot](./stage2/Queries/selectQueries/Medicinesindangerofexpiring/running.jpg)

![Query Results](./stage2/Queries/selectQueries/Medicinesindangerofexpiring/result.jpg)

### 7. For Each Item, How Many Warehouses Is It Located In

**שאילתה זו מזהה פריטים שנמצאים במספר רב של מחסנים שונים. היא מסייעת בזיהוי פריטים פופולריים שדורשים ניהול מלאי מורכב יותר. התוצאות מציגות עבור כל פריט את מספר המחסנים שבהם הוא נמצא, מסודר לפי המספר הגבוה ביותר של מחסנים.**

![Query Execution Screenshot](./stage2/Queries/selectQueries/Foreachitemhowmanywarehousesisitlocatedin/running.jpg)

![Query Results](./stage2/Queries/selectQueries/Foreachitemhowmanywarehousesisitlocatedin/result.jpg)

### 8. Items to Pick by Warehouse for a Specific Employee

**שאילתה זו מציגה לעובד ספציפי (במקרה זה עובד מספר 1) את כל הפריטים שעליו לאסוף ממחסנים שיש לו גישה אליהם, עבור הזמנות פתוחות של המחלקות שבהן הוא עובד. היא מסייעת לעובד לתכנן את מסלול האיסוף היעיל ביותר. התוצאות מציגות עבור כל מחסן את כל הפריטים לאיסוף, כולל הכמות הנדרשת והכמות הקיימת במלאי.**

![Query Execution Screenshot](./stage2/Queries/selectQueries/Itemstopickbywarehouseforaspecificemployee/running.jpg)

![Query Results](./stage2/Queries/selectQueries/Itemstopickbywarehouseforaspecificemployee/result.jpg)

## UPDATE Operations

### 1. Update Old Urgent Items

**עדכון של מצב פריט ההזמנה למאושר עבור כל פריטי ההזמנה הדחופים שהוגשו לפני שלושה ימים ולא אושרו (אפשר גם עבור ציוד רפואי)**

שאילתה זו מאשרת באופן אוטומטי פריטי הזמנה דחופים שהוגשו לפני יותר משלושה ימים אך טרם אושרו. פעולה זו מבטיחה שפריטים קריטיים לא נתקעים בתהליך האישור.

![לפני העדכון](./stage2/Queries/updateQueries/updateOldUrgent/Before.jpg)

![אחרי העדכון](./stage2/Queries/updateQueries/updateOldUrgent/After.jpg)

### 2. Update Popular Drugs

**מעלה את כמות התרופה במלאי אוטומטית עבור תרופות פופולריות**

שאילתה זו מגדילה את רמות המלאי עבור תרופות שמוזמנות בתדירות גבוהה. המערכת מגדילה באופן אוטומטי את כמויות המלאי של תרופות שמופיעות במספר רב של הזמנות.

![לפני העדכון](./stage2/Queries/updateQueries/updatePopularDrugs/Before.jpg)

![אישור העדכון](./stage2/Queries/updateQueries/updatePopularDrugs/Done.jpg)

![אחרי העדכון](./stage2/Queries/updateQueries/updatePopularDrugs/After.jpg)

### 3. Update Urgent Orders

**עדכון של מצב פריט ההזמנה למאושר עבור כל פריטי ההזמנה הדחופים שהוגשו על ידי מחלקות דחופות באופן ישיר**

שאילתה זו מאשרת באופן אוטומטי פריטי הזמנה דחופים שהוגשו על ידי מחלקות חירום. פעולה זו מייעלת את תהליך האישור עבור בקשות רגישות לזמן ממחלקות טיפול קריטי.

![לפני העדכון](./stage2/Queries/updateQueries/updateUrgentOrders/Before.jpg)

![אישור העדכון](./stage2/Queries/updateQueries/updateUrgentOrders/Done.jpg)

![אחרי העדכון](./stage2/Queries/updateQueries/updateUrgentOrders/After.jpg)

## Delete Operations

### 1. Delete Expired Orders

**מחיקה של כל ההזמנות (כולל תתי הזמנות) של כל ההזמנות שעברו שבועיים מעת הגשתם**

שאילתה זו מסירה הזמנות שגילן עולה על שבועיים מתאריך ההגשה שלהן. פעולת ניקוי זו מסייעת לשמור על יעילות בסיס הנתונים ומסירה נתונים ישנים שאינם רלוונטיים יותר למערכת.

![Before Deletion](stage2/Queries/deleteQueries/deleteExpiredOrders/Before.jpg)

![Confirmation](stage2/Queries/deleteQueries/deleteExpiredOrders/Done.jpg)

![After Deletion](stage2/Queries/deleteQueries/deleteExpiredOrders/After.jpg)

### 2. Delete Workers Without Warehouse Access

**מחיקת כל העובדים ללא גישה לשום מחסן**

שאילתה זו מזהה ומסירה עובדי לוגיסטיקה שאין להם גישה לאף מחסן, שכן הם אינם יכולים לבצע את תפקידם ביעילות ללא גישה כזו. פעולה זו מנקה את מערכת ניהול העובדים ומאפשרת התמקדות בעובדים פעילים.

![Before Deletion](stage2/Queries/deleteQueries/deleteNoAccessWorkers/Before.jpg)

![Confirmation](stage2/Queries/deleteQueries/deleteNoAccessWorkers/Done.jpg)

![After Deletion](stage2/Queries/deleteQueries/deleteNoAccessWorkers/After.jpg)


### 3. Delete delivered orders

**מחיקת כל ההזמנות שכל תתי ההזמנות שבהן סופקו**

כל הזמנה מורכבת מתתי הזמנות שונות. כל תת הזמנה יכולה להיות בסטטוס של ממתינה לאישור מאושרת ונשלחה.
אם המערכת זיהתה שיש הזמנה שכל תתי ההזמנות שבה כבר נשלחו אין טעם לשמור את ההזמנה לכן היא וכל תתי ההזמנות
שבה נמחקות.


![Before Deletion](stage2/Queries/deleteQueries/deleteAllDeliveredOrders/Before.jpg)

![Confirmation](stage2/Queries/deleteQueries/deleteAllDeliveredOrders/Done.jpg)

![After Deletion](stage2/Queries/deleteQueries/deleteAllDeliveredOrders/After.jpg)


## Constraints

The database system implements several constraints using ALTER TABLE commands to ensure data integrity and enforce business rules. Each constraint was tested by attempting to insert conflicting data to verify proper error handling.

### 1. Drug Stock Date Validation (chk_since)

**לא ניתן לרשום תרופה שהוכנסה למלאי עם תאריך עתידי (מחר או יותר).**

שינוי זה נעשה באמצעות פקודת ALTER TABLE על טבלת drug_in_stock, שמוסיפה אילוץ CHECK שמוודא שהתאריך בשדה 'since' אינו גדול מהתאריך הנוכחי. כאשר מנסים להכניס רשומה עם תאריך עתידי, המערכת מחזירה שגיאה ולא מאפשרת את ההכנסה.

```sql
ALTER TABLE drug_in_stock 
ADD CONSTRAINT chk_since CHECK (since <= CURRENT_DATE);
```

![Constraint Error](./stage2/Constraints/DrugStockDate.jpg)

### 2. Drug Order Item Positive Amount (chk_drug_order_item_positive_amount)

**אי אפשר להזמין תרופה בכמות אפס או שלילית.**

שינוי זה נעשה באמצעות פקודת ALTER TABLE על טבלת drug_order_item, שמוסיפה אילוץ CHECK שמוודא שהכמות (amount) היא תמיד מספר חיובי. כאשר מנסים להזמין תרופה בכמות 0 או שלילית, המערכת מחזירה שגיאה.

```sql
ALTER TABLE drug_order_item 
ADD CONSTRAINT chk_drug_order_item_positive_amount CHECK (amount > 0);
```

![Constraint Error](./stage2/Constraints/DrugAmount0.jpg)

### 3. Equipment Order Item Positive Amount (chk_equipment_order_item_positive_amount)

**אי אפשר להזמין ציוד רפואי בכמות אפס או שלילית.**

שינוי זה נעשה באמצעות פקודת ALTER TABLE על טבלת equipment_order_item, שמוסיפה אילוץ CHECK שמוודא שהכמות (amount) היא תמיד מספר חיובי. כאשר מנסים להזמין ציוד בכמות לא חיובית, המערכת מחזירה שגיאה.

```sql
ALTER TABLE equipment_order_item 
ADD CONSTRAINT chk_equipment_order_item_positive_amount CHECK (amount > 0);
```

![Constraint Error](./stage2/Constraints/EqAmount0.jpg)

### 4. Default Urgent Drug Flag

**אם לא ציינו האם ההזמנה דחופה – המערכת תניח שהיא לא דחופה כברירת מחדל.**

שינוי זה נעשה באמצעות פקודת ALTER TABLE על טבלת drug_order_item, שמוסיפה ערך ברירת מחדל FALSE לשדה is_urgent. כאשר מכניסים רשומה חדשה ללא ציון ערך לשדה זה, המערכת מגדירה אותו אוטומטית כ-FALSE.

```sql
ALTER TABLE drug_order_item 
ALTER COLUMN is_urgent SET DEFAULT FALSE;
```

![Default Value](./stage2/Constraints/DefaultUrgentDrug.jpg)

### 5. Default Urgent Equipment Flag

**גם בציוד רפואי – אם לא צוין דחוף, המערכת תניח שההזמנה אינה דחופה.**

שינוי זה נעשה באמצעות פקודת ALTER TABLE על טבלת equipment_order_item, שמוסיפה ערך ברירת מחדל FALSE לשדה is_urgent. כאשר מכניסים רשומה חדשה ללא ציון ערך לשדה זה, המערכת מגדירה אותו אוטומטית כ-FALSE.

```sql
ALTER TABLE equipment_order_item 
ALTER COLUMN is_urgent SET DEFAULT FALSE;
```

![Default Value](./stage2/Constraints/DfaultUrgentEq.jpg)

### 6. Not Null Since Date (NOT NULL on since)

**חובה להזין תאריך כניסה (since) לכל תרופה שנכנסת למלאי. בלי זה – אין תוקף ואין מעקב.**

שינוי זה נעשה באמצעות פקודת ALTER TABLE על טבלת drug_in_stock, שמוסיפה אילוץ NOT NULL לשדה since. כאשר מנסים להכניס רשומה ללא תאריך כניסה למלאי, המערכת מחזירה שגיאה ולא מאפשרת את ההכנסה.

```sql
ALTER TABLE drug_in_stock 
ALTER COLUMN since SET NOT NULL;
```

![Constraint Error](./stage2/Constraints/NullSinceDrugStock.jpg)


## Transaction Management

The hospital logistics system implements transaction management to ensure data integrity during complex operations that involve multiple related tables.

### COMMIT Example

The following example demonstrates a transaction that successfully commits changes to the database:

![Before Commit](./stage2/RollbackCommit/Commit/Update.jpg)

![Commit Operation](./stage2/RollbackCommit/Commit/Commiting.jpg)

![Changes Saved](./stage2/RollbackCommit/Commit/UpdateSaved.jpg)

The SQL code for this operation:

```sql
-- Example from ./stage2/RollbackCommit/Commit/CommitingExample.sql
BEGIN;
-- Operations performed within the transaction
UPDATE drug_in_stock SET amount = amount + 50 WHERE drug_id = 1 AND warehouse_id = 1;
-- Additional operations...
COMMIT;
```

### ROLLBACK Example

This example shows a transaction that is rolled back, discarding changes:

![Before Rollback](./stage2/RollbackCommit/RollBack/Updated.jpg)

![Rollback Operation](./stage2/RollbackCommit/RollBack/RollingBack.jpg)

![After Rollback](./stage2/RollbackCommit/RollBack/AfterRollingBack.jpg)

The SQL code for this operation:

```sql
-- Example from ./stage2/RollbackCommit/RollBack/RollingExample.sql
BEGIN;
-- Operations performed within the transaction
UPDATE drug_in_stock SET amount = amount - 30 WHERE drug_id = 1 AND warehouse_id = 1;
-- Due to an error or decision, changes are discarded
ROLLBACK;
```

Transaction management ensures that complex operations affecting multiple tables either complete successfully or have no effect at all, preserving data consistency in the hospital logistics system.


# Stage 3: Database Integration and Views""

The third stage of the Hospital Medical Equipment Logistics System project focuses on integrating two separate database systems and creating meaningful views that combine data from both systems.

## Table of Contents for Stage 3""

- [Integration Process](#integration-process)
- [Views](#views)
 - [Births Summary View](#births-summary-view)
 - [Department Equipment Orders View](#department-equipment-orders-view)
- [Project Structure for Stage 3](#project-structure-for-stage-3)

## Integration Process""

### Integration Decisions and Methodology""

During the integration process, we merged two distinct database systems:
- **Database A"": Medical Equipment Logistics System (our original project) - A general logistics management system for hospital departments
- **Database B"": Maternity Department Management System (from the other team) - A specialized system for maternity ward operations

**Integration Strategy:""**
Our projects complemented each other perfectly: while our system handles general hospital department logistics, their system focuses specifically on maternity ward operations. We identified that the most logical integration approach was to use inheritance, where the maternity department would be a specialized type of general department.

**Key Integration Approach:""**
We implemented an include/exclude inheritance pattern where:
1. The `maternity_department` entity inherits from our general `department` entity
2. This allows maternity departments to have all the general department capabilities plus specialized maternity features
3. We connected the `room` entity as a weak entity dependent on `maternity_department`
4. This creates a relationship where each maternity department has many rooms, and each room belongs to exactly one department

**Why This Design Makes Sense:""**
- Maintains data integrity by ensuring rooms cannot exist without a department
- Allows for specialized maternity functionality while preserving general department operations
- Enables seamless integration without duplicating existing department logic
- Provides a scalable model for adding other specialized departments in the future

### Entity Relationship Diagrams""

#### Original ERD - Our System""
![Original ERD Our System](./stage3/images_after/erd.png)

#### Original ERD - Other Team's System""
![Original ERD Other Team](./stage3/other_team_images/erd.png)

#### Updated DSD After Integration""
![Updated DSD After Integration](./stage3/images_after/dsd.png)

#### Original DSD - Other Team's System""
![Original DSD Other Team](./stage3/other_team_images/dsd.png)

### Technical Integration Process""

**Database Merging:""**
The integration was accomplished by restoring both database backups into a single database. Since there were no overlapping table names or conflicting schemas, the merge was straightforward.

**Schema Modifications:""**
The connection process required several critical schema changes:

1. **Creating the Maternity Department Table:""**
  - Created `maternity_department` as a specialization of `department`
  - Added maternity-specific attributes like `delivery_types_supported` and `birth_support_level`

2. **Modifying the Room Entity:""**
  - Added `department_id` as a foreign key to establish the weak entity relationship
  - Changed the primary key of `room` to composite key `(id_r, department_id)`
  - This ensures rooms are uniquely identified within their department context

3. **Updating Related Entities:""**
  - Modified `maternity` table to include `department_id` and update foreign key references
  - Updated `attending_to` table to include `department_id` in its primary key
  - Ensured all foreign key relationships maintained referential integrity

**Integration Commands Explained:""**

```sql""
-- Step 1: Create the specialized maternity_department table
CREATE TABLE maternity_department (
   department_id INT PRIMARY KEY REFERENCES department(department_id) ON DELETE CASCADE,
   delivery_types_supported TEXT[],
   birth_support_level TEXT
);

-- Step 2: Populate with sample maternity departments
INSERT INTO maternity_department (department_id, delivery_types_supported, birth_support_level) VALUES
(396, ARRAY['natural', 'epidural', 'c-section'], 'intermediate'),
(390, ARRAY['natural', 'epidural', 'c-section', 'VBAC', 'induced'], 'full'),
(341, ARRAY['natural', 'c-section'], 'basic');

-- Step 3: Add department_id to room table
ALTER TABLE room ADD COLUMN IF NOT EXISTS department_id integer;

-- Step 4: Set default department for existing rooms
UPDATE room SET department_id = 341 WHERE department_id IS NULL;

-- Step 5: Make department_id required
ALTER TABLE room ALTER COLUMN department_id SET NOT NULL;

-- Step 6: Drop existing constraints before modification
ALTER TABLE maternity DROP CONSTRAINT IF EXISTS maternity_id_r_fkey;
ALTER TABLE attending_to DROP CONSTRAINT IF EXISTS attending_to_id_r_fkey;
ALTER TABLE room DROP CONSTRAINT IF EXISTS room_pkey;

-- Step 7: Create composite primary key for room
ALTER TABLE room ADD CONSTRAINT room_pkey PRIMARY KEY (id_r, department_id);

-- Step 8: Add foreign key constraint to maternity_department
ALTER TABLE room ADD CONSTRAINT room_department_fk
   FOREIGN KEY (department_id) REFERENCES maternity_department (department_id)
   ON UPDATE CASCADE ON DELETE CASCADE;

-- Step 9: Update maternity table with department_id
ALTER TABLE maternity ADD COLUMN IF NOT EXISTS department_id integer;
UPDATE maternity m SET department_id = r.department_id
FROM room r WHERE m.id_r = r.id_r AND m.department_id IS NULL;
ALTER TABLE maternity ALTER COLUMN department_id SET NOT NULL;

-- Step 10: Update foreign key for maternity to reference composite key
ALTER TABLE maternity ADD CONSTRAINT maternity_room_fk
   FOREIGN KEY (id_r, department_id) REFERENCES room (id_r, department_id)
   ON UPDATE CASCADE ON DELETE RESTRICT;

-- Step 11: Update attending_to table similarly
ALTER TABLE attending_to ADD COLUMN IF NOT EXISTS department_id integer;
UPDATE attending_to a SET department_id = r.department_id
FROM room r WHERE a.id_r = r.id_r AND a.department_id IS NULL;
ALTER TABLE attending_to ALTER COLUMN department_id SET NOT NULL;

-- Step 12: Update attending_to primary key and foreign key
ALTER TABLE attending_to DROP CONSTRAINT IF EXISTS attending_to_pkey;
ALTER TABLE attending_to ADD CONSTRAINT attending_to_pkey PRIMARY KEY (id_r, department_id, id_n);
ALTER TABLE attending_to ADD CONSTRAINT attending_to_room_fk
   FOREIGN KEY (id_r, department_id) REFERENCES room (id_r, department_id)
   ON UPDATE CASCADE ON DELETE RESTRICT;
```""

## Views""

### Births Summary View""

**View Description:""**
The `births_summary_view` combines information about births, mothers, and doctors from the maternity department database. This view provides a comprehensive overview of birth records including mother details, doctor information, and birth outcomes.

**View Structure:""**
- Retrieves all birth records from `birth_record` table
- Joins with mother information from `maternity` table
- Connects births to attending doctors through `midwife` table
- Includes doctor details from `doctor` table

**Sample Data from View:""**
```sql""
SELECT * FROM births_summary_view LIMIT 10;
```""

![Births Summary View Output](./stage3/Views/births_summary_view/view_output.png)

#### Query 1: Doctor Specialization and Birth Statistics""

**Description:""**
This query counts how many births each doctor performed grouped by their specialization and calculates the average mother age for births they attended. It provides insights into doctor workload distribution across different specializations.

**SQL Query:""**
```sql""
SELECT 
   doctor_specialization,
   COUNT(DISTINCT doctor_id) as doctor_count,
   COUNT(record_id) as total_births,
   ROUND(AVG(mother_age), 1) as avg_mother_age
FROM births_summary_view
GROUP BY doctor_specialization
ORDER BY total_births DESC;
```""

![Query 1 Output](./stage3/Views/births_summary_view/Query1_output.png)

#### Query 2: Recent Normal Births by Experienced Doctors""

**Description:""**
This query identifies normal births performed in the last 6 months by doctors with at least 10 years of seniority. It helps track routine deliveries handled by experienced medical staff.

**SQL Query:""**
```sql""
SELECT 
   doctor_name,
   doctor_seniority,
   birth_date,
   mother_name,
   mother_age,
   birth_type
FROM births_summary_view
WHERE birth_type = 'Normal'
   AND birth_date >= CURRENT_DATE - INTERVAL '6 months'
   AND doctor_seniority >= 10
ORDER BY birth_date DESC;
```""

![Query 2 Output](./stage3/Views/births_summary_view/Query2_output.png)

### Department Equipment Orders View""

**View Description:""**
The `department_equipment_orders_view` consolidates equipment order information from the logistics database. It provides a unified view of all medical equipment orders placed by different departments, including order status and urgency flags.

**View Structure:""**
- Combines equipment order items from `equipment_order_item` table
- Includes order ID, department ID, equipment ID, quantity, status, and urgency flag
- Designed for analyzing equipment order history by departments

**Sample Data from View:""**
```sql""
SELECT * FROM department_equipment_orders_view LIMIT 10;
```""

![Department Equipment Orders View Output](./stage3/Views/department_equipment_orders_view/view_output.png)

#### Query 1: Unfulfilled Equipment Demand by Department""

**Description:""**
This query shows for each department how much equipment of each type they ordered (that hasn't been delivered yet) and counts how many of these orders are urgent. It helps prioritize urgent orders and understand unmet demand for each equipment type.

**SQL Query:""**
```sql""
SELECT 
   department_id,
   equipment_id,
   SUM(quantity) as total_quantity_ordered,
   COUNT(CASE WHEN is_urgent = TRUE THEN 1 END) as urgent_orders,
   COUNT(*) as total_orders
FROM department_equipment_orders_view
WHERE status != 'Delivered'
GROUP BY department_id, equipment_id
ORDER BY urgent_orders DESC, total_quantity_ordered DESC;
```""

![Query 1 Output](./stage3/Views/department_equipment_orders_view/Query1_output.png)

#### Query 2: Equipment Orders from High-Priority Departments""

**Description:""**
This query identifies equipment orders from departments with emergency level 3 or higher. It provides information about the ordering department, equipment name, quantity, urgency status, and order status.

**SQL Query:""**
```sql""
SELECT 
   d.department_id,
   d.department_name,
   e.equipment_name,
   deo.quantity,
   deo.is_urgent,
   deo.status
FROM department_equipment_orders_view deo
JOIN department d ON deo.department_id = d.department_id
JOIN medical_equipment e ON deo.equipment_id = e.equipment_id
WHERE d.emergency_level >= 3
ORDER BY deo.is_urgent DESC, deo.quantity DESC;
```""

![Query 2 Output](./stage3/Views/department_equipment_orders_view/Query2_output.png)

## Project Structure for Stage 3""

```""
stage3/
├── backup/
│   └── backup3
├── commands/
│   └── integration.sql
├── images_after/
│   ├── dsd.png
│   └── erd.png
├── other_team_images/
│   ├── dsd.png
│   └── erd.png
├── Views/
│   ├── births_summary_view/
│   │   ├── births_summary_view.sql
│   │   ├── Query_1.sql
│   │   ├── Query_2.sql
│   │   ├── Query1_output.png
│   │   ├── Query2_output.png
│   │   └── view_output.png
│   └── department_equipment_orders_view/
│       ├── department_equipment_orders_view.sql
│       ├── Query_1.sql
│       ├── Query_2.sql
│       ├── Query1_output.png
│       ├── Query2_output.png
│       └── view_output.png
└── README.md
```""

## Integration SQL Commands""

The complete integration process is documented in the `integration.sql` file, which includes:
- Table creation statements for the maternity_department specialization
- Schema modifications to implement the weak entity relationship for rooms
- Updates to foreign key constraints to maintain referential integrity
- View creation statements for unified data access
- Sample queries demonstrating the integrated functionality

This integration successfully combines the medical equipment logistics system with the maternity department management system, creating a comprehensive hospital management solution that supports both general department operations and specialized maternity care requirements.