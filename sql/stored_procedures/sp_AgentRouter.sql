-- NERVA Agent Router
-- Routes all agent requests to the correct stored procedure
-- Called by Azure Logic App on behalf of all 5 NERVA agents

CREATE PROCEDURE dbo.sp_AgentRouter
    @Action     VARCHAR(50),
    @OrderID    VARCHAR(20) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    IF @Action = 'getOrderStatus'
        EXEC dbo.sp_GetOrderStatus @OrderID = @OrderID;

    ELSE IF @Action = 'getSLARiskOrders'
        EXEC dbo.sp_GetSLARiskOrders;

    ELSE IF @Action = 'getCarrierAnomalies'
        EXEC dbo.sp_GetCarrierAnomalies;

    ELSE IF @Action = 'getImmuneScan'
        EXEC dbo.sp_GetImmuneScanData;

    ELSE IF @Action = 'getActiveOrdersByCarrier'
        EXEC dbo.sp_GetActiveOrdersByCarrier @CarrierID = @OrderID;

END
