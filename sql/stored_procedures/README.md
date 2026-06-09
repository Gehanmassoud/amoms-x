# NERVA Stored Procedures

sp_AgentRouter          Routes all agent requests by @Action parameter
sp_GetOrderStatus       Returns full order details by OrderID
sp_GetSLARiskOrders     Returns all at-risk orders
sp_GetCarrierAnomalies  Returns carrier anomaly patterns
sp_GetImmuneScanData    Returns full immune scan dataset
sp_LogAgentDecision     Writes to AgentLog observability table
sp_CreateImmuneAlert    Creates immune alert record
sp_UpdateDeliveryStatus Updates delivery record
sp_UpdateSLAStatus      Updates SLA status record