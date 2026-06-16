CREATE OR ALTER PROCEDURE sp_GetSLARiskOrders
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        OrderID,
        CustomerName,
        Priority,
        SLAStatus,
        DueDate,
        Carrier
    FROM SLA
    WHERE SLAStatus IN ('At Risk', 'Critical')
    ORDER BY DueDate ASC;
END
GO