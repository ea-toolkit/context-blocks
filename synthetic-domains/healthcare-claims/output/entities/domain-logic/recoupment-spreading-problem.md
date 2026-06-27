---
type: domain-logic
id: recoupment-spreading-problem
name: Recoupment Spreading Problem
description: |-
  Flawed logic for distributing large recoupments across payment cycles that doesn't coordinate multiple simultaneous recoupments
status: proposed
tags:
- payment-processing
- business-logic
- provider-experience
- needs-review
source_documents:
- design-session-payment-reconciliation.txt
confidence: 0.85
enforced_by:
- payment-engine
related_to:
- payment-threshold-rules
---

# Recoupment Spreading Problem

## Overview

Current recoupment spreading logic distributes large recoupments over multiple payment cycles when they exceed 50% of payment amount, but doesn't account for other recoupments in flight. This can result in providers receiving essentially no payments for extended periods when multiple recoupments hit simultaneously.

## Details

The spreading algorithm also interacts poorly with the $5 minimum payment threshold - unclear whether payments below threshold due to recoupment spreading should be held or sent as $0 payments (current behavior). Team identified this as more complex than initially understood, requiring consideration of fraud holds, provider payment volumes, and overall provider experience. Example given: provider with $50K monthly payments shouldn't be zeroed out by two $30K recoupments hitting the same cycle. Deferred to follow-up session with fraud team involvement.

## Open Questions

- Is the current $0 payment behavior for sub-threshold amounts intentional or a bug?
- How should fraud holds interact with recoupment spreading calculations?
