# ATP Calculation Policy
Document ID: INV-ATP-001

## ATP Formula
ATP = QuantityOnHand minus ReservedQuantity minus SafetyStockMinimum

## Safety Stock Minimums
- Fast moving items over 100 units per week: 20% of weekly demand
- Standard items 10 to 100 units per week: 10% of weekly demand
- Slow moving items under 10 units per week: 5 units minimum

## Validation Steps
1. Query SQL Inventory table for QuantityOnHand and ReservedQuantity
2. Confirm real-time availability
3. If values differ by over 5% use the lower value
4. Apply safety stock deduction
5. If ATP is greater than or equal to order quantity: Available
6. If ATP is less than order quantity but greater than zero: Partial
7. If ATP is zero or negative: Shortage

## Reservation Rules
- Reservation held maximum 48 hours without confirmed payment
- Enterprise customers: reservation held 7 days
- Reservations released automatically if order cancelled
