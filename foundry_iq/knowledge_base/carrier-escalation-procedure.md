# Carrier Escalation Procedure
Document ID: OPS-CARRIER-001

## When to Escalate
Carrier escalation is triggered when:
- Delivery ETA breach is confirmed
- Carrier has not provided update within 2 hours
- Customer has called to report non-delivery
- Immune Agent has published sla.breach or sla.critical event

## Escalation Priority Matrix
- Order value over $50,000 plus Enterprise tier: P1 Immediate, 15 minutes
- Order value over $10,000 plus Premium tier: P2 Urgent, 2 hours
- Order value over $1,000 plus Premium tier: P3 High, 4 hours
- Standard tier any value: P4 Normal, 24 hours

## Escalation Steps
1. Contact primary carrier account manager directly
2. Provide: OrderID, tracking number, committed window, breach duration
3. Request immediate status update and revised ETA
4. If no ETA within 30 minutes: activate backup carrier
5. Update delivery status in system
6. Notify customer via Coordination Agent

## Backup Carriers by Region
- Northeast US: FedEx Priority then UPS Next Day then regional carrier
- Southeast US: UPS Ground then FedEx Ground then USPS Priority
- West Coast: FedEx Priority then OnTrac then regional carrier
- Midwest: UPS then FedEx then regional carrier network
