:setvar ProjectSQL "C:\Users\fredd\Documents\Uni\CITS3401 Data Warehousing\Project\"
:setvar DatabaseName "CrimeIncidents"

PRINT '';
PRINT '*** Dropping Database';
GO

IF EXISTS (SELECT [name] FROM [master].[sys].[databases] WHERE [name] = 'CrimeIncidents')
DROP DATABASE CrimeIncidents;
GO
PRINT '';
PRINT '*** Creating Database';
GO
Create database CrimeIncidents
Go
Use CrimeIncidents
Go 
--dim tables
CREATE TABLE DimCrime
(
    crimekey INT PRIMARY KEY IDENTITY,
    crime VARCHAR(50),
    crime_severity INT
)
GO

Create table DimDate
(
    datekey INT PRIMARY KEY IDENTITY,
    year INT,
	year_quarter VARCHAR(3),
    month VARCHAR(9),
    weekday_weekend VARCHAR(7),
    day_of_week VARCHAR(9),
    date VARCHAR(10),
    day INT
)
Go


CREATE TABLE DimLocation1 (
    loc1key INT PRIMARY KEY IDENTITY,
    npu VARCHAR(1),
    neighborhood VARCHAR(50)
)
GO


CREATE TABLE DimLocation2 (
  loc2key INT PRIMARY KEY IDENTITY,
  country VARCHAR(50),
  state VARCHAR(50),
  city VARCHAR(50),
  county VARCHAR(50),
  road VARCHAR(50)
)
GO

--insert statements
BULK INSERT [dbo].[DimCrime]
FROM '$(ProjectSQL)dimcrime.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,
	KEEPIDENTITY
);


BULK INSERT [dbo].[DimDate]
FROM '$(ProjectSQL)dimdate.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,
	KEEPIDENTITY
);

PRINT 'Loading [dbo].[DimDate]';


BULK INSERT [dbo].[DimLocation1]
FROM '$(ProjectSQL)dimloc1.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,
	KEEPIDENTITY,
    TABLOCK
);

PRINT 'Loading [dbo].[DimLocation1]';


BULK INSERT [dbo].[DimLocation2]
FROM '$(ProjectSQL)dimloc2.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,
	KEEPIDENTITY
);

PRINT 'Loading [dbo].[DimLocation2]';

--fact table
PRINT '';
PRINT '*** Creating Table FactCrime';
GO
Create Table FactCrime
(
id bigint primary key IDENTITY(0,1) not null,
crimekey int not null,
datekey int not null,
loc1key int not null,
loc2key int not null,
countn int not null
)
Go
PRINT '';
PRINT '*** Add relation between fact table foreign keys to Primary keys of Dimensions';
GO
ALTER TABLE FactCrime ADD CONSTRAINT
FK_crimekey FOREIGN KEY (crimekey) REFERENCES DimCrime(crimekey);

ALTER TABLE FactCrime ADD CONSTRAINT
FK_datekey FOREIGN KEY (datekey) REFERENCES DimDate(datekey);

ALTER TABLE FactCrime ADD CONSTRAINT
FK_loc1key FOREIGN KEY (loc1key) REFERENCES DimLocation1(loc1key);

ALTER TABLE FactCrime ADD CONSTRAINT
FK_loc2key FOREIGN KEY (loc2key) REFERENCES DimLocation2(loc2key);

Go

BULK INSERT [dbo].[FactCrime]
FROM '$(ProjectSQL)fact.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,
	KEEPIDENTITY
);

PRINT 'Loading [dbo].[FactCrime]';
