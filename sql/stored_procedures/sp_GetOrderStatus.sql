-- Returns full order details for a specific OrderID
-- Called by: Intelligence Agent, Reasoning Agent, Voice Agent

CREATE PROCEDURE dbo.sp_GetOrderStatus
    @OrderID VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        o.OrderID,
        o.CustomerID,
        o.CustomerTier,
        o.OrderValue,
        o.Status,
        o.RequiredDate,
        d.CarrierName,
        d.ScheduledETA,
        d.DelayMinutes,
        s.SLAStatus,
        s.BreachRisk
    FROM dbo.Orders o
    LEFT JOIN dbo.Deliveries d ON o.OrderID = d.OrderID
    LEFT JOIN dbo.SLA s ON o.OrderID = s.OrderID
    WHERE o.OrderID = @OrderID;
END
