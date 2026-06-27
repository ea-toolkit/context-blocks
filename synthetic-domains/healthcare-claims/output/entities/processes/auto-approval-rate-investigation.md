---
type: process
id: auto-approval-rate-investigation
name: Auto-Approval Rate Investigation Process
description: Process to investigate and resolve drops in Pre-Auth Service auto-approval
  rates
status: active
tags:
- operational
- investigation
- clinical
source_documents:
- pre-auth-runbook.txt
confidence: 0.9
triggered_by:
- auto-approval-rate-drop
---

# Auto-Approval Rate Investigation Process

## Overview

Systematic investigation process for auto-approval rate degradation, focusing on clinical criteria changes and benefit plan data accuracy. Includes version comparison, service category analysis, and coordination with clinical teams.

## Details

Investigation steps: 1) Check criteria_load_history table to identify recent clinical criteria file updates, 2) Download and diff the last two criteria versions from gs://clearview-preauth-config/criteria/ to identify changes, 3) Run service category analysis query to identify which categories experienced approval rate drops, 4) If one category shows significant decline (e.g., imaging from 70% to 20%), coordinate with clinical team to verify intentional criteria tightening vs configuration error, 5) If rates dropped across all categories, investigate Eligibility Service for incorrect benefit plan assignments causing auth denials.
