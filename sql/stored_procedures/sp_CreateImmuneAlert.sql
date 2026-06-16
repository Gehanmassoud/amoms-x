CREATE OR ALTER PROCEDURE sp_CreateImmuneAlert
(
    @AlertType      VARCHAR(100),
    @Severity       VARCHAR(50),
    @Description    NVARCHAR(MAX),
    @DetectedBy     VARCHAR(100)
)
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO ImmuneAlerts
    (
        AlertType,
        Severity,
        Description,
        DetectedBy,
        CreatedAt
    )
    VALUES
    (
        @AlertType,
        @Severity,
        @Description,
        @DetectedBy,
        GETDATE()
    );
END
GO