# AMOMS-X
## Autonomous Multi-Agent Operations Management System — Extended

> *"The enterprise agent mesh that acts before you know there is a problem."*

**Hackathon:** Microsoft Agents League @ AI Skills Fest 2026  
**Tracks:** Reasoning Agents · Enterprise Agents · Creative Apps  
**IQ Layers:** Foundry IQ · Work IQ · Fabric IQ  
**Author:** Gehan Massoud  
**Repository:** github.com/Gehanmassoud/amoms-x

---

## The Problem

Every day, logistics and supply chain operations teams face the same crisis:

- A customer calls asking where their order is
- A support agent checks 3 different systems manually
- By the time the answer is found, the SLA has already breached
- Three other orders with the same root cause are not flagged
- The account manager for a $2M customer finds out from the customer

This is not a data problem. Every piece of information needed exists somewhere. It is a coordination problem.

**AMOMS-X solves it with one insight: every customer interaction is an autonomous enterprise intelligence trigger — not just a question to answer.**

---

## The Solution

AMOMS-X is a decentralized enterprise agent mesh where 5 specialized autonomous agents collaborate through Azure Event Grid, reason independently through Azure AI Foundry grounded in all three Microsoft IQ layers, and operate on a governed data foundation — with Microsoft Purview DSPM auditing every agent decision.

**No central orchestrator. No single point of failure. No ungoverned decisions.**

### What happens when a customer calls

```
Customer calls → Voice Agent answers
      ↓
Pulls live order data from Azure SQL via Logic App
      ↓
Answers customer with accurate information
      ↓ simultaneously
Publishes order.customer_inquiry to Azure Event Grid
      ↓
SLA Agent activates → queries Foundry IQ for policy
                    → verifies Fabric IQ semantics
                    → produces 5-step cited reasoning chain
                    → detects breach → escalates
      ↓
Notification Agent → notifies account manager
      ↓
Immune Agent → scans for related patterns proactively
```

---

## The 5 Agents

| Agent | Purpose | Key capability |
|---|---|---|
| Dynamics Data Agent | Live data retrieval | Azure SQL via Logic App router |
| SLA Monitor Agent | 5-step reasoning chain | Foundry IQ citations + semantic verification |
| Immune Agent | Proactive anomaly detection | Acts before anyone asks |
| Notification Agent | Targeted communications | P1-P4 escalation matrix |
| Voice Agent | Inbound call handling | Triggers autonomous mesh cascade |

---

## The Immune Agent — The Wow Moment

While every other agent reacts to events, the Immune Agent acts before events happen.

It scans carrier performance data every 15 minutes unprompted and detects failure patterns before any SLA breaches.

When it detects FedEx Northeast showing 7 delay events with 94% confidence:

```
AMOMS-X IMMUNE ALERT — Unprompted Detection
Carrier: FedEx Northeast
Pattern: 7 delay events in 6 hours
Confidence: 94%
Revenue at risk: $383,000

I have autonomously:
- Initiated P1 escalation
- Published risk.emerging to Event Grid
- Requested executive approval via Copilot Studio

No one asked me to do this. I noticed.
```

---

## Microsoft IQ Integration

### Foundry IQ
- Knowledge base: kb-amosx-prod with 10 policy documents
- SLA Agent queries Foundry IQ before every decision
- Every decision is grounded and cited — never hallucinated

### Work IQ
- Surfaces organizational context for high-value accounts
- Notification Agent finds the right account manager automatically

### Fabric IQ
- Ontology defines 5 canonical business entities
- Every agent reasons from the same semantic definitions
- Eliminates inter-agent semantic drift

**Remove any one IQ layer and the system breaks. All three are load-bearing.**

---

## Architecture

```
Security + Governance: Entra ID, Key Vault, Purview DSPM
         |
Microsoft IQ Layer: Foundry IQ, Work IQ, Fabric IQ
         |
Azure Event Grid — Decentralized Agent Mesh Spine
         |
5 Autonomous Agents — Azure AI Foundry GPT-4.1-mini
         |
Integration Layer: Logic App Router, API Management
         |
Data Layer: Azure SQL, Dynamics 365
```

---

## How It Meets the Rubric

| Criterion | Weight | How AMOMS-X scores |
|---|---|---|
| Accuracy and Relevance | 20% | Foundry IQ citations ground every decision |
| Reasoning and Multi-step | 20% | 5-step SLA chain with dual Foundry IQ citations |
| Creativity and Originality | 15% | Voice cascade trigger plus Immune Agent wow moment |
| UX and Presentation | 15% | Copilot Studio dashboard plus voice interface |
| Reliability and Safety | 20% | Purview DSPM, Managed Identities, stored procedures only |
| Community Vote | 10% | The system that noticed before anyone asked |

---

## Technologies Used

**AI and Agents:** Azure AI Foundry, GPT-4.1-mini, Foundry IQ, Work IQ, Fabric IQ

**Azure Platform:** Event Grid, Logic Apps, API Management, Azure SQL, Key Vault, Entra ID, Managed Identities, Purview DSPM

**Development:** GitHub Copilot VS Code, Python, REST APIs

**Microsoft 365:** Copilot Studio, Power BI

---

## Infrastructure Notes

### Azure SQL Server Region
The SQL Server is named sql-amosx-prod-eus but is physically deployed in West US due to East US regional capacity constraints at time of creation. All agents connect correctly.

---

## Setup

### Prerequisites
- Azure subscription
- Microsoft 365 tenant with Copilot Studio access

### Environment Variables
Copy .env.example to .env and fill in your values. Never commit .env

### Key Resources
- Azure AI Foundry project: aif-amosx-prod-eus
- SQL Database: db-amosx-prod on sql-amosx-prod-eus
- Foundry IQ KB: kb-amosx-prod
- Event Grid: evgns-amosx-prod-eus

---

## Demo Video
Link to be added before submission

---

## Hack for Good

AMOMS-X applies directly to humanitarian logistics. The same Immune Agent that prevents a carrier failure in commercial logistics prevents 340 families from missing a meal delivery in food bank operations. The same Purview governance that protects commercial customer data protects the identities of vulnerable beneficiaries.

---

## License
MIT License — see LICENSE file

Built during Microsoft Agents League @ AI Skills Fest 2026
Developed with GitHub Copilot
