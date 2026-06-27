---
type: domain-logic
id: adjudication-disposition-rules
name: Adjudication Disposition Rules
description: Logic determining PAY/DENY/PEND outcomes from rules engine evaluation
status: active
tags:
- decision-logic
- automation-target
- vendor-migration
source_documents:
- claims-processing-workflow.txt
confidence: 0.9
enforced_by:
- rules-engine
produces:
- claim-adjudicated-event
---

# Adjudication Disposition Rules

## Overview

Decision logic that evaluates benefit rules, provider contracts, medical policies, and accumulators to produce one of three claim dispositions. Target is 85% auto-adjudication rate.

## Details

The rules engine evaluates multiple factors to determine claim disposition: PAY disposition when service is covered, provider is contracted/rates available, medical policies are met, and member has remaining benefits. DENY disposition when service is excluded, provider requirements aren't met, medical necessity isn't established, or member lacks coverage/benefits. PEND disposition when manual review is needed for complex scenarios, missing information, or edge cases the automated rules can't resolve. The current auto-adjudication rate is 81% against an 85% target, with the gap primarily due to incomplete rule migration from the vendor system replacement project. Pended claims go to claims adjudicator queue for manual determination.
