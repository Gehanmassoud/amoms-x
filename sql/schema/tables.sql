-- NERVA / AMOMS-X Database Schema
-- Azure SQL Database: db-amosx-prod
-- All agent access via stored procedures only

CREATE TABLE dbo.Orders (
    OrderID         VARCHAR(20)     PRIMARY KEY,
    CustomerID      VARCHAR(20)     NOT NULL,
    CustomerTier    VARCHAR(20)     NOT NULL,
    OrderValue      DECIMAL(12,2)   NOT NULL,
    Status          VARCHAR(20)     NOT NULL,
    RequiredDate    DATETIME        NOT NULL,
    CreatedAt       DATETIME        DEFAULT GETDATE()
);

CREATE TABLE dbo.Inventory (
    ProductID           VARCHAR(20)     PRIMARY KEY,
    ProductName         VARCHAR(100)    NOT NULL,
    QuantityOnHand      INT             NOT NULL,
    ReservedQuantity    INT             DEFAULT 0,
    SafetyStockMinimum  INT             DEFAULT 0,
    UnitCost            DECIMAL(10,2)   NOT NULL
);

CREATE TABLE dbo.Deliveries (
    DeliveryID      VARCHAR(20)     PRIMARY KEY,
    OrderID         VARCHAR(20)     NOT NULL REFERENCES dbo.Orders(OrderID),
    CarrierID       VARCHAR(20)     NOT NULL,
    CarrierName     VARCHAR(100)    NOT NULL,
    ScheduledETA    DATETIME        NOT NULL,
    ActualETA       DATETIME        NULL,
    DelayMinutes    INT             DEFAULT 0,
    Status          VARCHAR(20)     NOT NULL
);

CREATE TABLE dbo.SLA (
    SLAID           VARCHAR(20)     PRIMARY KEY,
    OrderID         VARCHAR(20)     NOT NULL REFERENCES dbo.Orders(OrderID),
    SLAStatus       VARCHAR(20)     NOT NULL,
    BreachRisk      DECIMAL(5,2)    DEFAULT 0,
    HoursRemaining  DECIMAL(8,2)    NULL,
    LastEvaluated   DATETIME        DEFAULT GETDATE()
);

CREATE TABLE dbo.AgentLog (
    LogID           INT             IDENTITY(1,1) PRIMARY KEY,
    AgentName       VARCHAR(50)     NOT NULL,
    DecisionType    VARCHAR(50)     NOT NULL,
    InputData       NVARCHAR(MAX)   NULL,
    ReasoningChain  NVARCHAR(MAX)   NULL,
    FoundryIQCitation VARCHAR(200)  NULL,
    FabricIQEntity  VARCHAR(100)    NULL,
    Decision        NVARCHAR(MAX)   NULL,
    Confidence      DECIMAL(5,2)    NULL,
    EventPublished  VARCHAR(100)    NULL,
    ExecutionMs     INT             NULL,
    CreatedAt       DATETIME        DEFAULT GETDATE()
);

CREATE TABLE dbo.CarrierPerformance (
    RecordID        INT             IDENTITY(1,1) PRIMARY KEY,
    CarrierID       VARCHAR(20)     NOT NULL,
    CarrierName     VARCHAR(100)    NOT NULL,
    Region          VARCHAR(50)     NOT NULL,
    EventTime       DATETIME        NOT NULL,
    DelayMinutes    INT             NOT NULL,
    Resolved        BIT             DEFAULT 0,
    AffectedOrderID VARCHAR(20)     NULL
);

CREATE TABLE dbo.ImmuneAlerts (
    AlertID         INT             IDENTITY(1,1) PRIMARY KEY,
    ThreatType      VARCHAR(50)     NOT NULL,
    Severity        VARCHAR(20)     NOT NULL,
    CarrierID       VARCHAR(20)     NULL,
    PatternConfidence DECIMAL(5,2)  NOT NULL,
    AffectedOrders  INT             DEFAULT 0,
    AffectedRevenue DECIMAL(14,2)   DEFAULT 0,
    AutonomousActions NVARCHAR(MAX) NULL,
    PendingApprovals NVARCHAR(MAX)  NULL,
    Status          VARCHAR(20)     DEFAULT 'Active',
    CreatedAt       DATETIME        DEFAULT GETDATE()
);
