CREATE OR ALTER PROCEDURE sp_ProceduralMemory
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        MemoryID,
        AgentName,
        ScenarioType,
        Resolution,
        Confidence,
        CreatedAt
    FROM ProceduralMemory
    ORDER BY CreatedAt DESC;
END
GO