# NERVA

## The Autonomous Enterprise Nervous System

### Powered by AMOMS-X: Autonomous Multi-Agent Organizational Meta-System Extended

Contextualize. Anticipate. Intervene. Evolve.

An unprompted immune agent mesh that diagnoses the $1M failure forming from a $10K signal, mitigating second-order consequences and preventing third-order failures across any domain.

**Flagship Experience:** [**NERVA Resonance**](https://nerva-resonance.com/)
Explore the futures your decisions create.

Hackathon: Microsoft Agents League @ AI Skills Fest 2026
Tracks: Reasoning Agents, Enterprise Agents, Creative Apps
IQ Layers: Foundry IQ, Work IQ, Fabric IQ
Author: Gehan Massoud
Repository: github.com/Gehanmassoud/amoms-x

[View Architecture Diagram](https://github.com/Gehanmassoud/amoms-x/blob/main/NERVA%20Architecture%20Diagram.pdf)

\---

## The Vision

Most enterprise AI answers questions.
NERVA prevents the questions from needing to be asked.

NERVA introduces the concept of enterprise immunity.

NERVA is a self-protecting enterprise agent mesh that continuously monitors organizational health, contextualizes operational signals, anticipates emerging consequence cascades, intervenes before failures occur, and evolves through organizational learning.

NERVA does not wait for a failure to happen.
NERVA does not wait to be asked.
NERVA patrols.

\---

## The Four Principles

CONTEXTUALIZE
NERVA continuously builds and maintains a Shared Enterprise Context from operational data, organizational relationships, policies, business semantics, and institutional knowledge. Through Foundry IQ, Work IQ, and Fabric IQ, every signal is interpreted within its full organizational context rather than in isolation.

NERVA does not see events. It understands their meaning.

ANTICIPATE
NERVA continuously evaluates emerging patterns, organizational dependencies, and consequence cascades before they become visible failures. Rather than reacting to incidents, NERVA identifies the conditions that create them and explores potential future outcomes before they occur.

The goal is not prediction. The goal is anticipation.

INTERVENE
When risk thresholds are exceeded, NERVA generates policy-grounded interventions through Consequence Cascade Reasoning. Every recommendation is validated against enterprise policy, verified against semantic context, evaluated for business impact, and coordinated across the agent mesh before action is taken.

Every intervention is explainable, traceable, and auditable.

EVOLVE
NERVA captures every decision, mitigation strategy, and outcome as reusable organizational knowledge. Through Procedural Memory and Organizational Learning, successful interventions become part of the enterprise's institutional intelligence, improving resilience and decision quality over time.

Every intervention makes the system smarter.

\---

## Consequence Cascade Reasoning

Consequence Cascade Reasoning is NERVA's ability to predict second-order and third-order business impacts from a single event before those impacts become visible to humans.

When a carrier delay is detected, NERVA does not record a delay. It evaluates what happens next if no action is taken, what happens if partial action is taken, and what happens if full intervention is executed. It selects the path with the lowest consequence footprint, executes it, and captures the outcome as organizational memory.

This is the reasoning architecture that separates NERVA from every other enterprise AI system.

\---

## Shared Enterprise Context

NERVA continuously constructs and maintains a Shared Enterprise Context using Work IQ, Fabric IQ, and Foundry IQ simultaneously. This context models the organization as a living graph of interconnected entities:

People: employees, teams, roles, skills, reporting relationships
Work: projects, tasks, deadlines, deliverables, dependencies
Business: customers, vendors, contracts, revenue streams
Governance: risks, decisions, policies, compliance obligations

The Immune Agent reasons over this Shared Enterprise Context continuously. It traverses entity relationships to identify emerging organizational threats before they become operational failures. When a critical employee leaves, the context immediately surfaces every project, deliverable, and customer relationship that depends on them. When a vendor becomes a bottleneck, it shows every team and timeline affected.

This is not a dashboard. This is organizational awareness.

\---

## The Problem It Solves

Organizations fail silently. Not because data is missing. Because no system connects the signals until it is too late.

Operational failures:

* A carrier degrades over 6 hours and 47 orders are affected before anyone notices
* A medication stock trends toward zero and a ward runs short at 2am
* A fraud pattern forms across 3 accounts and the transaction completes

Organizational failures:

* A lead architect resigns and 3 critical projects silently lose their only expert
* A vendor bottleneck appears across 4 unrelated teams but no one sees the connection
* A release deadline approaches while knowledge transfer is never scheduled

NERVA detects all of these. Before the failure. Without being asked.

\---

## The Solution

No central orchestrator. No single point of failure. No ungoverned decisions.

Agents communicate peer-to-peer through Azure Event Grid. There is no master agent, no central controller, no single point of failure. When the Immune Agent detects a threat, it publishes an event and every other agent in the mesh decides independently how to respond.

The mesh operates in two modes:

REACTIVE MODE: When a customer calls, the entire mesh activates to answer and resolve.
IMMUNE MODE: Every 15 minutes, the Immune Agent scans the Shared Enterprise Context for failure patterns nobody asked about.

\---

## The Immune Agent: Two Types of Detection

The Immune Agent detects two categories of organizational failure. Both unprompted. Both before anyone asks.

OPERATIONAL DETECTION: Real output from the live NERVA system:

&#x20;   NERVA IMMUNE ALERT: Unprompted Detection
    Threat type: CarrierAnomaly
    Carrier: FedEx Northeast
    Pattern: 7 delay events in 6 hours
    Average delay: 40 minutes
    Confidence: 94%
    Revenue at risk: $383,000

    I have autonomously:
    - Initiated P1 escalation per carrier-escalation-procedure.md
    - Published risk.emerging event to Azure Event Grid
    - Requested executive approval via NERVA Command Center

    No one asked me to do this. I noticed.


ORGANIZATIONAL DETECTION: What NERVA detects beyond logistics:

&#x20;   NERVA IMMUNE ALERT: Unprompted Detection
    Threat type: OrganizationalRisk
    Pattern detected:
      Lead architect resigned
      3 critical projects depend on this architect
      Knowledge transfer not scheduled
      Release deadline in 17 days
      No backup owner identified

    Predicted impact:
      72% probability of release delay
      Estimated revenue exposure: $1,400,000

    I have autonomously:
    - Created knowledge transfer task via Work IQ
    - Identified backup engineer via Fabric IQ entity graph
    - Alerted VP Engineering via Risk Response Agent
    - Published risk.emerging to Event Grid

    No one asked me to do this. I noticed.


This is enterprise intelligence. Not logistics management.

\---

## Two Modes. One Nervous System.

### IMMUNE MODE: No trigger required

Every 15 minutes, with no human prompt and no customer call,
the Immune Agent scans the Shared Enterprise Context across
all 28 organizational entities and 41 dependency relationships.

It does not wait for a signal. It looks for the conditions
that create signals.

When the Immune Agent detects a failure signature:

1. Immune Agent traverses Fabric IQ entity graph unprompted
2. Detects emerging pattern: carrier degradation, organizational
dependency collapse, SLA clustering, inventory depletion
3. Calculates consequence cascade: second and third order impacts
4. Publishes risk.emerging to Azure Event Grid
5. Reasoning Agent activates and executes 5-step chain
6. Risk Response Agent routes P1-P4 escalation via Work IQ
7. NERVA Command Center surfaces approval in Copilot Studio

The customer never called.
No ticket was opened.
No alert had fired.
No human knew there was a problem.

NERVA noticed.

\---

### REACTIVE MODE: What happens when a customer calls

1. Customer calls and Voice Agent answers
2. Context Agent pulls live order data from Azure SQL
and Dynamics 365 via Logic App
3. Voice Agent answers customer with accurate information
4. Simultaneously publishes order.customer\_inquiry to Azure Event Grid
5. Reasoning Agent activates, queries Foundry IQ for policy,
verifies Fabric IQ semantics, produces 5-step cited
Consequence Cascade Reasoning chain
6. Risk Response Agent alerts the right account manager via Work IQ
7. Immune Agent scans the Shared Enterprise Context for related
organizational patterns

By the time the customer hangs up, the root cause has been
identified, the SLA has been re-evaluated, and three other
at-risk orders have been flagged proactively.

\---

## [NERVA Resonance](https://nerva-resonance.com/): The Living Enterprise

NERVA Resonance is the flagship interactive experience for exploring the Enterprise Consequence Graph powered by the Fabric IQ entity graph.

Employees, projects, risks, vendors, customers, and decisions become nodes in a real-time organizational graph. Dependencies become connections. Emerging risks appear as consequence hotspots before failures occur. The Shared Enterprise Context becomes visible and explorable.

The NERVA Resonance allows executives, operators, and agents to simulate consequence cascades before they occur. Click any entity node and see: what happens if this node fails? What are the second-order impacts? What are the third-order impacts? What does intervention cost versus inaction?

Built with GitHub Copilot and powered by the Fabric IQ entity graph.

This is not a dashboard.
This is an immune system display.
This is the future of enterprise intelligence.

\---

## Why NERVA: Any Industry Where Failure Has Consequences

The same 5 agents. The same architecture. The same nervous system. Any domain.

|Industry|What NERVA Detects|Stakes|
|-|-|-|
|Supply chain|Carrier failure pattern before SLA breach|Revenue loss|
|Healthcare|Medication stock trending toward shortage|Patient safety|
|Manufacturing|Equipment signature before line stops|Downtime costs|
|Finance|Transaction pattern matching fraud signature|Financial loss|
|Humanitarian|Distribution disruption before families affected|Human crisis|
|Any enterprise|Organizational dependency failure before it cascades|Strategic risk|

The entities change. The reasoning engine does not.

\---

## Microsoft IQ Integration

### Foundry IQ: The Knowledge Foundation

* Knowledge base: kb-amosx-prod with 10 enterprise policy documents
* Every agent decision grounded before execution, never after
* Reasoning Agent queries Foundry IQ at Step 2 of every reasoning chain
* Immune Agent queries Foundry IQ for escalation procedures on every detected threat
* Citation format: \[document-name, Policy ID, Section]
* Result: zero hallucinated decisions across the entire mesh

### Work IQ: The Organizational Intelligence Layer

* Surfaces who owns what across the organization
* Risk Response Agent queries Work IQ before every escalation
* Immune Agent uses Work IQ to identify backup owners when critical dependencies are at risk
* Escalations reach the right human automatically, not a generic inbox

### Fabric IQ: The Semantic Foundation

Ontology defines 12 canonical business entities: Order, Customer, Inventory, SLA, Carrier, Employee, Team, Project, Vendor, Contract, Risk, Decision.

The ontology is the semantic contract between agents and the structural foundation of the Shared Enterprise Context. When the Reasoning Agent says "Enterprise customer," when the Risk Response Agent says "account executive," and when the Immune Agent traverses project dependencies, all three are reasoning from the same Fabric IQ entity graph.

This eliminates semantic drift, the number one source of hallucinated decisions in multi-agent systems identified at FabCon 2026. It also enables graph reasoning across the entire organization, not just within a single domain.

Remove any one IQ layer and the system breaks architecturally. All three are load-bearing.

\---

## The 5 Agents

|Agent|Foundry ID|Mode|Purpose|Key Capability|
|-|-|-|-|-|
|Context Agent|ag-amosx-dynamics-prod|Both|Shared Enterprise Context retrieval|Azure SQL + Dynamics 365 via Logic App router|
|Reasoning Agent|ag-amosx-sla-prod|Reactive|5-step Consequence Cascade Reasoning chain|Foundry IQ citations + Fabric IQ semantic verification|
|Immune Agent|ag-amosx-immune-prod|Immune|Proactive anomaly detection every 15 min|Operational and organizational risk detection|
|Risk Response Agent|ag-amosx-notify-prod|Both|Targeted escalation and mitigation|Work IQ + P1-P4 escalation matrix|
|Voice Agent|ag-amosx-voice-prod|Reactive|Inbound call handling|Triggers autonomous mesh cascade via Event Grid|

Plus: NERVA Command Center (Copilot Studio) serving as the human-in-the-loop governance layer inside Copilot Studio. The five agents coordinate themselves through Azure Event Grid. The Command Center provides human oversight, approval workflows, and executive visibility. It does not orchestrate the agents.

\---

## Reasoning Agent: 5-Step Consequence Cascade Reasoning Chain

Every step is logged, cited, and auditable.

Step 1 DETECT: Query Azure SQL for at-risk orders via Context Agent
Step 2 RETRIEVE POLICY: Query Foundry IQ, return cited policy document with exact policy ID and section
Step 3 VERIFY SEMANTICS: Confirm entity classification via Fabric IQ ontology
Step 4 DECIDE: Evaluate consequence trajectories, produce decision with confidence score and full citation chain
Step 5 LEARN: Write complete reasoning artifact to AgentLog and Procedural Memory via stored procedure

Real output for Premium order ORD-1009:

&#x20;   STEP 2 POLICY RETRIEVAL:
    Policy Found: AMOMS-X SLA Policy, Premium Tier
    Citation: SLA-PREM-002, Section 3.1
    Required Action: Escalate to Tier 2 support and notify customer within 2 hours

    STEP 3 SEMANTIC VERIFICATION:
    Customer qualifies as Premium: YES
    Verification: CONFIRMED

    STEP 4 DECISION:
    Escalation Level: P2
    Confidence: 85%
    Revenue at risk: $150,000
    Event to Publish: sla.atrisk
    Citations: \[SLA-PREM-002 Section 3.1] \[fabric-iq/entity\_Customer]

    STEP 5 LEARN:
    Pattern: Premium + 3hrs + 45min delay = P2 escalation (85%)
    Decision logged: YES
    Procedural memory updated: YES


\---

## Agent Observability Genome

Every agent decision writes to the AgentLog with the complete reasoning record:

* Agent name and decision type
* Input data at time of decision
* Full reasoning chain
* Foundry IQ citation used
* Fabric IQ entity verified
* Final decision and confidence score
* Event published to Event Grid
* Execution time in milliseconds

\---

## Architecture

&#x20;   Security + Governance
             |
    Microsoft IQ Intelligence Layer
    Foundry IQ, Work IQ, Fabric IQ
    Shared Enterprise Context foundation
             |
    Azure Event Grid
    Decentralized Agent Mesh Spine
    Peer-to-peer A2A agent communication
    No central controller
             |
    5 Autonomous Agents
    Azure AI Foundry, GPT-4.1-mini
    Each reasons independently over the Shared Enterprise Context
             |
    Human-in-the-Loop Layer
    NERVA Command Center, Copilot Studio, Copilot Studio
    Executive visibility, approval workflows, natural language queries
             |
    Integration Layer
    Logic App Router, API Management
    Stored procedures only, sp\_AgentRouter single entry point
             |
    Data Layer
    Azure SQL, Dynamics 365-ready integration layer
             |
    Governance + Learning Layer
    AgentLog, RiskResponses, Procedural Memory
    Every decision captured, cited, and available for organizational learning


\---

## Security, Governance and Reliability

**Governed. Explainable. Secure. Traceable. Trustworthy.**

NERVA was designed with governance, security, traceability, reliability, and controlled autonomy as foundational architectural principles. The platform combines human-in-the-loop oversight, policy-grounded reasoning, organizational memory, explainable decision intelligence, and controlled data access patterns to ensure that autonomous intelligence remains accountable, transparent, and trustworthy.

|Control Area|Implementation|
|-|-|
|Governed Data Access|Controlled Logic App Agent Router integration boundary|
|Database Connectivity|No direct agent-to-database connectivity|
|Stored Procedure Access|Stored procedure-only access through sp\_AgentRouter|
|Layer Separation|Separation of reasoning, communication, and persistence layers|
|Agent Coordination|Event-driven agent coordination with controlled data access patterns|
|Human-in-the-Loop Governance|Human-in-the-loop governance for autonomous interventions|
|Policy Grounding|Policy-grounded decision intelligence through Foundry IQ|
|Shared Enterprise Context|Contextualized and policy-aware reasoning foundation|
|Explainable Reasoning|Reasoning chains with supporting evidence, policy citations, and consequence analysis|
|Decision Traceability|End-to-end decision traceability across multi-agent workflows|
|Audit Trail|AgentLog-backed audit trail for governance, accountability, and forensic review|
|Procedural Memory Traceability|Organizational learning, pattern reuse, and institutional knowledge retention|
|Intervention Governance|Controlled mitigation approval, escalation, and intervention workflows|
|Recommendation Safety|Confidence-scored recommendations with transparent decision rationale|
|Access Control Design|Architecture aligned with least-privilege access patterns|
|Secret Management|Azure Key Vault-ready secret management architecture|
|Consequence Transparency|Transparent consequence intelligence and intervention justification|

### Responsible AI

NERVA incorporates Responsible AI principles through governed decision intelligence, explainable reasoning, human oversight, and transparent intervention workflows. Key controls include human-in-the-loop governance, policy-grounded reasoning, explainable decision chains, decision traceability, confidence-scored recommendations, AgentLog auditability, controlled mitigation approval workflows, and organizational memory transparency.

\---

## Reliability and Safety

|Layer|Implementation|
|-|-|
|Identity|Azure Managed Identities, no secrets in code|
|Database|Stored procedures only, no direct table writes|
|Secrets|Azure Key Vault, never hardcoded|
|Sensitivity|PII labels automatically enforced|
|Lineage|Full trace from data source to output|
|Network|API Management with throttling and rate limiting|
|Learning|Procedural Memory captures decision patterns for reuse|

\---

## Accessibility

NERVA incorporates accessibility and industry independence as first-class capabilities, ensuring that enterprise intelligence, consequence analysis, governance workflows, and organizational learning remain accessible to a broad range of users, stakeholders, and industries.

### Industry Independence by Design

NERVA was designed as a domain-agnostic enterprise nervous system rather than a solution for a single industry. The platform contextualizes signals, anticipates consequences, recommends interventions, and evolves organizational learning across any operational environment without requiring changes to the core architecture.

The same architecture can be applied to:

* Supply Chain
* Healthcare
* Humanitarian Response
* Financial Services
* Cybersecurity
* Technology Operations
* Workforce and HR
* Critical Infrastructure
* Public Sector
* Any future enterprise domain

Rather than modeling a specific business process, NERVA models how organizations detect signals, understand context, anticipate consequences, coordinate interventions, and learn from outcomes. This allows the NERVA Agent Mesh, Procedural Memory, Command Center, Voice Agent, and NERVA Resonance to operate consistently across industries while adapting to domain-specific knowledge through Foundry IQ, Work IQ, Fabric IQ, and enterprise context sources.

### Explainable AI

All decisions are presented as structured reasoning chains including operational signals, policy citations, business impact, confidence levels, recommended interventions, and organizational learning references, ensuring transparency and accessibility for both technical and non-technical stakeholders.

### Voice-First Interaction

The NERVA Voice Agent enables hands-free access to enterprise intelligence through natural language conversations. Users can request consequence analysis, query organizational context, review reasoning chains, inspect policy citations, and approve or reject mitigations without requiring traditional dashboard interactions.

### Natural Language Governance

NERVA Command Center supports voice-driven governance workflows, allowing users to perform operational actions including approving or rejecting mitigations, requesting additional analysis, and escalating for executive review through natural language commands. This enables human-in-the-loop governance without requiring users to navigate complex operational systems.

### Consequence Narration

NERVA can narrate consequence trajectories using natural language.

Example interaction:

&#x20;   "NERVA, explain the impact of this decision."

    Response: "A 45-minute delay has increased the probability
    of SLA breach to 70%. If no action is taken, revenue
    exposure may reach $150,000. Recommended intervention:
    Tier 2 escalation per SLA-PREM-002 Section 3.1."


This enables consequence intelligence to be consumed through voice interactions rather than requiring visual analysis.

### Screen Reader Friendly Design

NERVA Resonance is designed using semantic interface principles supporting structured consequence explanations, keyboard navigation, screen-reader-friendly reasoning outputs, and accessible presentation of policy citations and governance decisions.

\---

## Rubric Compliance

|Criterion|Weight|How NERVA Scores|
|-|-|-|
|Reasoning and Multi-step|20%|5-step Consequence Cascade Reasoning chain, logged, cited, dual IQ verification, Shared Enterprise Context graph traversal|
|Creativity and Originality|15%|NERVA Resonance + Consequence Cascade Reasoning + immune detection + organizational risk detection|
|UX and Presentation|15%|Voice interface + NERVA Command Center + Resonance dashboard + accessible design|
|Community Vote|10%|The system that noticed before anyone asked|

\---

## Keywords

Azure AI Foundry, Foundry IQ, Work IQ, Fabric IQ,
Multi-Agent System, Autonomous Agents, A2A Architecture,
Azure Event Grid, Consequence Cascade Reasoning,
Immune Detection, Proactive Risk Detection,
5-Step Reasoning Chain, Grounded Reasoning, Policy Citation,
Semantic Verification, Procedural Memory, AgentLog,
Logic Apps, Azure SQL, Stored Procedures,
Voice Live, Voice Agent, Copilot Studio, Copilot Studio,
Human-in-the-Loop, GitHub Copilot, AI-Assisted Development,
NERVA Resonance, Enterprise Consequence Graph,
Accessibility, WCAG, Keyboard Navigation,
Shared Enterprise Context, Industry Independent,
Supply Chain, Healthcare, Humanitarian, Hack for Good,
Responsible AI, Explainable AI, SLA Breach Prevention,
Carrier Anomaly Detection, Organizational Risk Detection

\---

## Technologies Used

### AI and Agents

|Technology|Purpose|
|-|-|
|Azure AI Foundry|Agent hosting and orchestration|
|GPT-4.1-mini|Reasoning model for all 5 autonomous agents|
|Foundry IQ|Policy grounding, kb-amosx-prod, 10 documents, Answer synthesis|
|Work IQ|Organizational graph, escalation routing, Work IQ User and Mail tools|
|Fabric IQ|Semantic entity ontology, 12 entity types, Shared Enterprise Context|

### Azure Platform

|Technology|Purpose|
|-|-|
|Azure Event Grid|A2A peer-to-peer agent mesh spine|
|Azure Logic Apps|Agent Router, sp\_AgentRouter, single SQL entry point|
|Azure SQL Database|7 tables, 9 stored procedures, AgentLog observability|
|Azure AI Search|Foundry IQ index|
|Azure Key Vault|Centralized secret management, all credentials at runtime|
|Microsoft Entra ID|Agent identity, Managed Identities, no secrets in code|
|API Management|Rate limiting and throttling|

### Development

|Technology|Purpose|
|-|-|
|GitHub Copilot|Built voice\_agent.py (148L), sla\_monitor.py (178L), immune\_agent.py, context\_agent.py, risk\_response\_agent.py, session recorded|
|VS Code|Primary development environment|
|Python 3|Agent implementation language|
|Git|Version control|
|REST APIs|OpenAPI tool connections for all agents|

### Microsoft 365 and Copilot

|Technology|Purpose|
|-|-|
|Copilot Studio|NERVA Command Center, human-in-the-loop governance|
|Copilot Studio|Agent deployment and executive visibility channel|
|Voice Live|Azure Speech, Ava Dragon HD, Voice Agent inbound calls|

### Creative and Visualization

|Technology|Purpose|
|-|-|
|NERVA Resonance|Enterprise Consequence Graph, HTML Canvas API, physics simulation, consequence cascade, keyboard navigation, high contrast, ARIA live regions, WCAG AA accessible, built with GitHub Copilot|
|NERVA Dashboard|Unified front-end demo application, live agent feed, Event Grid visualization|

### Data and Governance

|Technology|Purpose|
|-|-|
|sp\_AgentRouter|Single SQL entry point for all agent operations|
|sp\_GetOrderStatus|Live order data retrieval|
|sp\_GetCarrierAnomalies|Carrier anomaly detection data|
|sp\_ProceduralMemory|Organizational learning capture|
|sp\_RiskResponse|Risk response logging|

\---

## Infrastructure Notes

The SQL Server is named sql-amosx-prod-eus but is physically deployed in West US due to East US regional capacity constraints at time of creation. All agents connect correctly through the Logic App router.

Azure Key Vault (kv-amosx-prod-eus) is deployed in East US and serves as the centralized secret management layer for all NERVA agents. All agent credentials, API keys, and connection strings are retrieved from Key Vault at runtime through Azure Managed Identities. No secrets are stored in code or committed to source control.

Dynamics 365 is included as an enterprise system-of-record integration point for customer, account, and service context. In the current build, Azure SQL acts as the live operational data source while the architecture is prepared for Dynamics 365 customer and account enrichment through the Shared Enterprise Context layer.

\---

## Repository Structure

&#x20;   amoms-x/
    agents/
      context\_agent.py         Context Agent - Shared Enterprise Context retrieval
                               Azure SQL + Dynamics 365-ready, built with GitHub Copilot
      immune\_agent.py          Immune Agent - proactive detection every 15 minutes
                               Built with GitHub Copilot
      risk\_response\_agent.py   Risk Response Agent - escalation, approval, mitigation
                               Built with GitHub Copilot
      sla\_monitor.py           Reasoning Agent - 5-step Consequence Cascade Reasoning
                               Built with GitHub Copilot
      voice\_agent.py           Voice Agent - inbound calls, cascade trigger
                               Built with GitHub Copilot
    foundry\_iq/
      knowledge\_base/
        README.md
        atp-calculation-policy.md        INV-ATP-001
        breach-escalation-matrix.md      SLA-ESC-001
        carrier-escalation-procedure.md  OPS-CARRIER-001
        humanitarian-logistics-protocol.md  OPS-HUM-001
        immune-detection-patterns.md     OPS-IMMUNE-001
        inventory-shortage-protocol.md   OPS-INV-001
        notification-templates.md        OPS-NOTIF-001
        sla-policy-enterprise.md         SLA-ENT-001
        sla-policy-premium.md            SLA-PRE-001
        sla-policy-standard.md           SLA-STD-001
    sql/
      schema/
        README.md
        tables.sql             7 tables including AgentLog observability table
      stored\_procedures/
        README.md
        sp\_AgentRouter.sql     Single entry point for all agent SQL operations
        sp\_GetCarrierAnomalies.sql
        sp\_GetOrderStatus.sql
    .env.example               Environment template, no real secrets committed
    LICENSE                    MIT License
    NERVA Architecture Diagram.pdf  Full 7-layer architecture diagram


## Setup

Prerequisites: Azure subscription, Microsoft 365 tenant with Copilot Studio access

Copy .env.example to .env and fill in values. Never commit .env.

Key resources:

* Azure AI Foundry: aif-amosx-prod-eus
* SQL Database: db-amosx-prod on sql-amosx-prod-eus
* Foundry IQ KB: kb-amosx-prod
* Event Grid: evgns-amosx-prod-eus
* Key Vault: kv-amosx-prod-eus

\---

## Demo Video

https://www.youtube.com/watch?v=n8YidYu6cU0

\---

## Hack for Good

NERVA was designed to be industry-independent by design.

The same architecture that protects revenue, service levels, and operational continuity inside enterprises can also support organizations operating in environments where the consequences are measured not only in dollars, but in human outcomes.

NERVA's ability to contextualize signals, anticipate consequences, coordinate interventions, and evolve organizational learning can be applied across:

* Humanitarian Response
* Disaster Relief
* Food Distribution Networks
* Healthcare Operations
* Critical Infrastructure
* Public Sector Services
* Community Support Organizations

A delayed shipment, a resource shortage, a service interruption, or a coordination failure may appear as isolated events. NERVA evaluates how those signals propagate through interconnected systems, identifies emerging risks, and recommends interventions before the consequences escalate.

The mission remains the same regardless of domain:

Detect earlier. Understand deeper. Intervene sooner. Learn continuously.

Whether protecting enterprise operations or supporting communities during times of need, NERVA provides organizations with the ability to see beyond immediate events and understand the consequences that follow.

\---

## License

MIT License, see LICENSE file

Built during Microsoft Agents League @ AI Skills Fest 2026
Developed with GitHub Copilot

