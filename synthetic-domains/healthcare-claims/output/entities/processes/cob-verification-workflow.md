---
type: process
id: cob-verification-workflow
name: COB Verification Workflow
description: |-
  Five-step process for verifying and updating member COB information after auto-detection
status: planned
tags:
- member-communication
- compliance
source_documents:
- design-session-cob-handling.txt
confidence: 0.9
triggered_by:
- cob-detection-signals
executed_by:
- eligibility-service
involves:
- member-services
---

# COB Verification Workflow

## Overview

Workflow triggered when COB auto-detection flags a member for review. Includes member outreach, response handling, and claim reprocessing for confirmed other coverage.

## Details

Step 1: Member flagged for COB review by detection system. Step 2: Outreach via email and portal notification asking member to confirm other coverage. Step 3: If confirmed, update COB record and trigger reprocessing of recent claims where overpayment occurred. Step 4: If no response within 30 days, send physical letter. Step 5: If still no response, flag for manual review by Member Services rep. Step 3 reprocessing is expensive and must consider regulatory limits on recoupment (typically 12-18 months depending on state).
