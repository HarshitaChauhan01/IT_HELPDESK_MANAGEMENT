/*
    IT Help Desk Management System
    Database setup script

    Run this script in SQL Server Management Studio (SSMS).
    It creates the database and Tickets table if they do not exist.
*/

IF DB_ID(N'IT_HelpDesk') IS NULL
BEGIN
    CREATE DATABASE IT_HelpDesk;
END;
GO

USE IT_HelpDesk;
GO

IF OBJECT_ID(N'dbo.Tickets', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Tickets
    (
        Ticket_ID INT IDENTITY(1,1) PRIMARY KEY,
        Employee_Name VARCHAR(100) NOT NULL,
        Department VARCHAR(50),
        Issue_Category VARCHAR(50) NOT NULL,
        Description VARCHAR(500),
        Priority VARCHAR(20) NOT NULL,
        Status VARCHAR(30) DEFAULT 'Open',
        Created_Date DATETIME DEFAULT GETDATE(),
        Resolution_Date DATETIME NULL
    );
END;
GO
