---
type: process
id: cob-auto-detection-project
name: COB Auto-Detection Project
description: |-
  Project to automatically detect coordination of benefits scenarios, pushed to Q1 2026
status: planned
tags:
- domain-logic
- compliance
- cost-reduction
source_documents:
- meeting-notes-quarterly-ops-review-2025q3.txt
- eligibility-monitoring-guide.txt
- design-session-cob-handling.txt
confidence: 0.9
related_to: cob
supersedes: cob-questionnaire
owned_by: member-services
improves: cob-data-model
addresses: cob
requires:
- claims-gateway
- eligibility-service
---

# COB Auto-Detection Project

## Overview

Project to develop automated detection of coordination of benefits situations when members have coverage from multiple payers. Currently in design phase but pushed from Q4 2025 to Q1 2026.

## Details

Project aimed at automatically identifying coordination of benefits (COB) scenarios where members have health coverage from multiple insurance sources (e.g., spouse's employer plan, Medicare, etc.). Automatic detection would improve claim processing efficiency and reduce manual review requirements. The project was originally planned for Q4 2025 but has been pushed to Q1 2026, currently still in the design phase under Member Services team ownership.

## Additional Details
[from eligibility-monitoring-guide.txt]

Design project aimed at improving COB data accuracy by automatically detecting when members have other coverage, reducing reliance on low-response member questionnaires (~40% completion) and verification letters (~35% response). Still in design phase with documentation referenced as 'COB handling design session notes'. Intended to address ongoing COB data staleness and overpayment risks.

## Additional Details
[from design-session-cob-handling.txt]

Addresses the problem that COB data is stale for 30-40% of members with other coverage, with current verification methods (portal questionnaire at 40% completion, annual letters at 35% response) proving inadequate. The system will analyze five potential signals: (1) unusually low billed amounts suggesting other payer paid first, (2) service gaps in claim patterns, (3) pharmacy cross-reference data, (4) Medicare eligibility at age 65, and (5) spouse employment changes. Initial implementation focuses on signals #1 and #4 as most tractable. Scheduled for Q1 2026 implementation.
