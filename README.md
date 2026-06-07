# AMOMS-X
## Autonomous Multi-Agent Operations Management System Extended

"A decentralized autonomous agent mesh that detects operational failure before it occurs in any industry where time-sensitive operations have consequences for people."

Hackathon: Microsoft Agents League @ AI Skills Fest 2026
Tracks: Reasoning Agents, Enterprise Agents, Creative Apps
IQ Layers: Foundry IQ, Work IQ, Fabric IQ
Author: Gehan Massoud
Repository: github.com/Gehanmassoud/amoms-x

---

## The Problem

Every day, operations teams face the same crisis:

- A customer calls asking where their order is
- A support agent checks 3 different systems manually
- By the time the answer is found, the SLA has already breached
- Three other orders with the same root cause are not flagged
- The account manager for a $2M customer finds out from the customer

This is not a data problem. Every piece of information needed exists somewhere. It is a coordination problem.

AMOMS-X solves it with one insight: every customer interaction is an autonomous enterprise intelligence trigger, not just a question to answer.

---

## The Solution

AMOMS-X is a decentralized enterprise agent mesh where 5 specialized autonomous agents collaborate through Azure Event Grid, reason independently through Azure AI Foundry grounded in all three Microsoft IQ layers, and operate on a governed data foundation with Microsoft Purview DSPM auditing every agent decision.

No central orchestrator. No single point of failure. No ungoverned decisions.

---

## What Happens When a Customer Calls

1. Customer calls and Voice Agent answers
2. Pulls live order data from Azure SQL via Logic App
3. Answers customer with accurate information
4. Simultaneously publishes order.customer_inquiry to Azure Event Grid
5. SLA Agent activates, queries Foundry IQ for policy, verifies Fabric IQ semantics, produces 5-step cited reasoning chain
6. Notification Agent alerts account manager
7. Immune Agent scans for related patterns proactively

---

## The 5 Agents

| Agent | Purpose | Key Capability |
|---|---|---|
| Dynamics Data Agent | Live data retrieval | Azure SQL via Logic App router |
| SLA Monitor Agent | 5-step reasoning chain | Foundry IQ citations + semantic verification |
| Immune Agent | Proactive anomaly detection | Acts before anyone asks |
| Notification Agent | Targeted communications | P1-P4 escalation matrix |
| Voice Agent | Inbound call handling | Triggers autonomous mesh cascade |

---

## The Immune Agent: The Wow Moment

While every other agent reacts to events, the Immune Agent acts before events happen.

It scans carrier performance data every 15 minutes unprompted and detects failure patterns before any SLA breaches.

When it detects a carrier showing 7 delay events with 94% confidence:

    AMOMS-X IMMUNE ALERT: Unprompted Detection
    Carrier: FedEx Northeast (synthetic demo carrier)
    Pattern: 7 delay events in 6 hours
    Confidence: 94%
    Revenue at risk: $383,000

    I have autonomously:
    - Initiated P1 escalation
    - Published risk.emerging to Event Grid
    - Requested executive approval via Copilot Studio

    No one asked me to do this. I noticed.

---

## Why AMOMS-X: The X Stands for Extended

The same 5 agents. The same architecture. Any industry.

| Industry | What AMOMS-X Detects | Stakes |
|---|---|---|
| Supply chain | Carrier failure before SLA breach | Revenue loss |
| Healthcare | Medication shortage before ward runs out | Patient safety |
| Manufacturing | Equipment failure before line stops | Downtime costs |
| Finance | Fraud pattern before transaction completes | Financial loss |
| Humanitarian | Distribution disruption before families affected | Human crisis |

---

## Microsoft IQ Integration

### Foundry IQ
- Knowledge base: kb-amosx-prod with 10 policy documents
- SLA Agent queries Foundry IQ before every decision
- Every decision is grounded and cited, never hallucinated
- Citation format: [document-name, Policy ID, Section]

### Work IQ
- Surfaces organizational context for high-value accounts
- Notification Agent finds the right account manager automatically
- Escalations reach the right human, not a generic inbox

### Fabric IQ
- Ontology defines 5 canonical business entities: Order, Customer, Inventory, SLA, Carrier
- Every agent reasons from the same semantic definitions
- Eliminates inter-agent semantic drift, the number one source of enterprise AI hallucination

Remove any one IQ layer and the system breaks. All three are load-bearing.

---

## SLA Agent: 5-Step Reasoning Chain

Step 1 DETECT: Query SQL for at-risk orders
Step 2 RETRIEVE POLICY: Query Foundry IQ, returns cited policy document
Step 3 VERIFY SEMANTICS: Confirm customer tier via Fabric IQ ontology
Step 4 DECIDE: Produce escalation decision with confidence score and citations
Step 5 LOG: Write resolution pattern to agent memory

Example output for Enterprise order ORD-1009:

    STEP 2 POLICY RETRIEVAL:
    Policy Found: AMOMS-X SLA Policy, Enterprise Tier
    Citation: SLA-ENT-001, Section: Escalation Procedure
    Required Action: Immediate P1 escalation, crisis response protocol

    STEP 3 SEMANTIC VERIFICATION:
    Customer qualifies as Enterprise: YES (ARR $2,400,000)
    Verification: CONFIRMED

    STEP 4 DECISION:
    Escalation Level: P1
    Confidence: 98%
    Event to Publish: sla.critical

---

## Architecture

    Security + Governance: Entra ID, Key Vault, Purview DSPM
             |
    Microsoft IQ Layer: Foundry IQ, Work IQ, Fabric IQ
             |
    Azure Event Grid: Decentralized Agent Mesh Spine
             |
    5 Autonomous Agents: Azure AI Foundry GPT-4.1-mini
             |
    Integration Layer: Logic App Router, API Management
             |
    Data Layer: Azure SQL, Dynamics 365

---

## Rubric Compliance

| Criterion | Weight | How AMOMS-X Scores |
|---|---|---|
| Accuracy and Relevance | 20% | Foundry IQ citations ground every decision |
| Reasoning and Multi-step | 20% | 5-step SLA chain with dual Foundry IQ citations |
| Creativity and Originality | 15% | Voice cascade trigger + Immune Agent wow moment |
| UX and Presentation | 15% | Copilot Studio dashboard + voice interface |
| Reliability and Safety | 20% | Purview DSPM + Managed Identities + stored procedures only |
| Community Vote | 10% | The system that noticed before anyone asked |

---

## Technologies Used

AI and Agents: Azure AI Foundry, GPT-4.1-mini, Foundry IQ, Work IQ, Fabric IQ

Azure Platform: Event Grid, Logic Apps, API Management, Azure SQL, Key Vault, Entra ID, Managed Identities, Purview DSPM

Development: GitHub Copilot for VS Code, Python, REST APIs

Microsoft 365: Copilot Studio, Power BI

---

## Infrastructure Notes

The SQL Server is named sql-amosx-prod-eus but is physically deployed in West US due to East US regional capacity constraints at time of creation. All agents connect correctly.

---

## Repository Structure

    agents/
      voice_agent.py       Voice Live integration, built with GitHub Copilot
      sla_monitor.py       5-step reasoning chain
      immune_agent.py      Proactive anomaly detection
    sql/
      schema/              Table definitions
      stored_procedures/   All SQL access via stored procedures only
    foundry_iq/
      knowledge_base/      10 policy documents
    .env.example           Environment template, no real secrets

---

## Setup

Prerequisites: Azure subscription, Microsoft 365 tenant with Copilot Studio access

Copy .env.example to .env and fill in values. Never commit .env to the repository.

Key resources:
- Azure AI Foundry: aif-amosx-prod-eus
- SQL Database: db-amosx-prod on sql-amosx-prod-eus
- Foundry IQ KB: kb-amosx-prod
- Event Grid: evgns-amosx-prod-eus
- Key Vault: kv-amosx-prod-eus

---

## Demo Video

Link to be added before submission deadline June 14 2026

---

## Hack for Good

AMOMS-X applies directly to humanitarian logistics, food banks, disaster relief, and refugee supply chains.

The same Immune Agent that detects a carrier failure affecting $383,000 in commercial orders detects a distribution disruption affecting 340 families before they miss their weekly food delivery.

The same Purview governance that protects commercial customer PII protects the identities and locations of vulnerable beneficiaries.

Same system. Same agents. Infinitely higher stakes.

---

## License

MIT License, see LICENSE file

Built during Microsoft Agents League @ AI Skills Fest 2026
Developed with GitHub Copilot
