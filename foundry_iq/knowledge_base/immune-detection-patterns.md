# NERVA Immune Agent Detection Patterns
Document ID: OPS-IMMUNE-001

## Carrier Anomaly Pattern
Trigger conditions:
- 3 or more delay events of 15 minutes or more in 6 hours
- Pattern confidence calculation:
  7 or more events: 94% confidence
  5 to 6 events: 80% confidence
  3 to 4 events: 65% confidence

## Autonomous Actions Authorized
When confidence exceeds 70% and order value below $50,000:
- Reroute to backup carrier autonomously
- Notify account managers via Work IQ
- Update delivery records

When confidence exceeds 90% regardless of order value:
- Immediate P1 escalation
- Request executive approval via Copilot Studio
- Publish risk.emerging event to Event Grid

## SLA Cluster Pattern
Trigger: 3 or more orders enter Warning or Breach status within 2 hours
Action: Publish risk.emerging with type SLACluster
This indicates systemic issue not isolated incidents

## Organizational Risk Pattern
Trigger: Critical dependency node removed from entity graph (resignation, vendor failure, project cancellation)
Action: Traverse Fabric IQ entity graph to identify all downstream impacts
Predict failure probability and revenue exposure
Publish risk.emerging with type OrganizationalRisk

## Immune Agent Output Format
When critical threat detected output exactly:
NERVA IMMUNE ALERT: Unprompted Detection
Threat type: [CarrierAnomaly / SLACluster / OrganizationalRisk]
Severity: [CRITICAL / HIGH / MEDIUM]
Pattern: [description]
Confidence: [percentage]%
Revenue at risk: $[amount]
Autonomous actions taken: [list]
Awaiting approval for: [list]
No one asked me to do this. I noticed.
