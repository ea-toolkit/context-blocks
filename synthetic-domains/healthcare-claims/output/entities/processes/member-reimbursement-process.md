---
type: process
id: member-reimbursement-process
name: Member Reimbursement Process
description: |-
  Processing of member reimbursements for out-of-network claims within 10 business days
status: active
tags:
- member-service
- oon-processing
- timely-payment
source_documents:
- claims-processing-workflow.txt
confidence: 0.85
executed_by:
- payment-engine
serves:
- member
uses:
- member-portal
---

# Member Reimbursement Process

## Overview

Workflow for reimbursing members who paid providers upfront for out-of-network services. Processes payments within 10 business days via check or direct deposit.

## Details

For out-of-network (OON) claims where members paid providers upfront, the reimbursement process calculates the member's covered amount based on usual and customary rates and benefit plan terms. Reimbursements are processed within 10 business days of claim adjudication. Payment methods include check (default) or direct deposit if the member has set up ACH in the Member Portal. This process ensures members receive timely reimbursement for covered services they initially paid out-of-pocket, maintaining good member satisfaction for OON care scenarios.
