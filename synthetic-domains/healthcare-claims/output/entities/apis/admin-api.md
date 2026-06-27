---
type: api
id: admin-api
name: Admin API
description: |-
  Administrative API interface for manual adjustments requiring Member Services lead approval
status: active
tags:
- administrative
- manual-adjustments
- approval-required
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.85
used_for:
- member-escalation-process
modifies:
- accumulator
governed_by:
- member-services
---

# Admin API

## Overview

Administrative API used for manual adjustments to member accounts and accumulator corrections. Requires Member Services lead approval for sensitive operations like accumulator adjustments.

## Details

API interface used for administrative functions including manual accumulator adjustments when double-applied deductible or drift issues are detected. Operations require Member Services lead approval before execution, indicating elevated privilege level and audit requirements. Used to resolve complex member account issues that cannot be handled through normal automated processes.
