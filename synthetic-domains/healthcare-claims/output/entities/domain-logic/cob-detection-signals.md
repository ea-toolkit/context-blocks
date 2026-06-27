---
type: domain-logic
id: cob-detection-signals
name: COB Detection Signals
description: |-
  Five identified signals in claims data that indicate potential unreported other coverage
status: planned
tags:
- domain-logic
- detection-algorithm
source_documents:
- design-session-cob-handling.txt
confidence: 0.95
part_of:
- cob-auto-detection-project
uses:
- claim
---

# COB Detection Signals

## Overview

Business rules for automatically identifying members who likely have other insurance coverage they haven't reported. Five signals range from billed amount analysis to Medicare eligibility checks.

## Details

Signal #1: Unusually low billed amounts compared to 25th percentile for procedure code, suggesting another payer paid first. Signal #2: Service gaps where regular claim patterns suddenly stop. Signal #3: Pharmacy cross-reference showing different primary insurance. Signal #4: Medicare eligibility when member turns 65. Signal #5: Spouse employment changes from large employers. Initial implementation focuses on signals #1 and #4 as most tractable, with #2 being too noisy, #3 requiring pharmacy system integration, and #5 being impractical.
