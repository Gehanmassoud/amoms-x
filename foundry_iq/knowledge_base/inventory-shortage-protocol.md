# Inventory Shortage Protocol
Document ID: OPS-INV-001

## Shortage Detection
Shortage detected when:
- Available quantity minus reserved quantity is less than order quantity
- ATP calculation returns negative value
- Confirms shortage across all warehouse locations

## Response by Shortage Type

Partial Shortage (can fulfill over 50% of order):
1. Reserve available stock immediately
2. Split order: fulfill available now, backorder remainder
3. Notify customer of partial fulfillment and backorder ETA
4. Check alternate warehouse locations

Full Shortage (cannot fulfill any of order):
1. Do not reserve stock
2. Check incoming stock purchase orders in transit
3. If stock arriving within SLA window: hold order and confirm
4. If not arriving in time: escalate to Operations Manager
5. Offer alternatives: substitute product or cancellation

Critical Shortage (affects multiple orders):
1. Immediately publish inventory.critical event
2. Immune Agent evaluates all affected orders by tier priority
3. Allocate available stock to highest tier customers first
4. Operations Manager notified immediately
