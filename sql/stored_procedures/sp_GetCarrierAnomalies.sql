-- Detects carrier anomaly patterns from recent performance data
-- Called by: Immune Agent (every 15 minutes, unprompted)
-- Returns carriers with 3+ delay events in last 6 hours

CREATE PROCEDURE dbo.sp_GetCarrierAnomalies
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        cp.CarrierID,
        cp.CarrierName,
        cp.Region,
        COUNT(*)                        AS DelayCount,
        AVG(CAST(cp.DelayMinutes AS FLOAT)) AS AvgDelayMinutes,
        MAX(cp.DelayMinutes)            AS MaxDelayMinutes,
        COUNT(DISTINCT cp.AffectedOrderID) AS AffectedOrders,
        ISNULL(SUM(o.OrderValue), 0)    AS AffectedRevenue,
        CAST(
            CASE
                WHEN COUNT(*) >= 7 THEN 94.0
                WHEN COUNT(*) >= 5 THEN 80.0
                WHEN COUNT(*) >= 3 THEN 65.0
                ELSE 40.0
            END AS DECIMAL(5,2)
        )                               AS PatternConfidence
    FROM dbo.CarrierPerformance cp
    LEFT JOIN dbo.Orders o ON cp.AffectedOrderID = o.OrderID
    WHERE cp.EventTime >= DATEADD(HOUR, -6, GETDATE())
      AND cp.DelayMinutes >= 15
      AND cp.Resolved = 0
    GROUP BY cp.CarrierID, cp.CarrierName, cp.Region
    HAVING COUNT(*) >= 3
    ORDER BY PatternConfidence DESC;
END
