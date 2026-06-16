CREATE OR ALTER PROCEDURE sp_RiskResponse
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        ResponseID,
        RiskType,
        Severity,
        RecommendedAction,
        CreatedAt
    FROM RiskResponses
    ORDER BY CreatedAt DESC;
END
GO