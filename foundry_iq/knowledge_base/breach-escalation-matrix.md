# Breach Escalation Matrix
Document ID: SLA-ESC-001

## Decision Tree
Is customer Enterprise tier?
  Yes: Immediate P1 escalation regardless of order value

Is order value over $10,000 AND Premium tier?
  Yes: P2 escalation within 2 hours

Is breach duration over 24 hours?
  Yes: Critical escalation to Operations Manager

Otherwise: Standard escalation to logistics coordinator

## Notification Chain by Level

P1 Enterprise:
- Immediately: Account Executive via Work IQ
- 15 minutes: VP Operations
- 30 minutes: Customer executive contact
- 1 hour: COO briefed

P2 Premium High Value:
- Immediately: Account Manager via Work IQ
- 2 hours: Carrier escalation initiated
- 4 hours: Operations Manager if unresolved

P3 Premium Standard:
- Immediately: Automated customer notification
- 4 hours: Logistics coordinator assigned
- 8 hours: Account Manager if unresolved

P4 Standard:
- Immediately: Automated customer notification
- 24 hours: Logistics coordinator review

## Resolution Requirements
All escalations require:
- Resolution event published to Event Grid
- Customer confirmation of receipt
- Audit log entry via Purview DSPM
- Post-resolution report for P1 and P2
