---
type: external-party
id: healthlogic-systems
name: HealthLogic Systems
description: Vendor providing the Rules Engine system that Clearview is planning to
  replace
status: active
tags:
- vendor
- rules-engine
- slow-support
source_documents:
- claims-ops-contacts-and-escalation.txt
confidence: 0.95
provides:
- rules-engine
---

# HealthLogic Systems

## Overview

HealthLogic Systems is the vendor that provides the HealthLogic Rules Engine currently used by Clearview Health Plans. They provide enterprise support with defined SLAs but are noted as being slow to respond.

## Details

HealthLogic Systems is the vendor behind the HealthLogic Rules Engine (also known as HealthLogic Adjudicator) that Clearview currently uses for claims adjudication. The document provides detailed contact information including support email (support@healthlogicsystems.com), support phone ((800) 555-HLGC), and account manager Derek Foss (derek.foss@healthlogicsystems.com). Their SLA includes P1 = 4 hour response, P2 = 8 hour response. However, there's a warning that 'they're slow' and recommendations to call AND email for P1 issues, plus ping Derek directly. They also provide VPN tunnel support through infra-ops@healthlogicsystems.com. The fact that Clearview is actively migrating away from this system (per ADR-2024-007) suggests ongoing challenges with this vendor relationship.
