---
type: process
id: manual-auth-override
name: Manual Auth Override Process
description: |-
  Emergency process for manually approving authorizations with clinical lead approval
status: active
tags:
- emergency
- manual
- clinical
source_documents:
- pre-auth-runbook.txt
confidence: 0.95
involves:
- dr-sarah-lin
---

# Manual Auth Override Process

## Overview

Emergency procedure requiring Dr. Sarah Lin's written approval to manually override authorization decisions. Includes database updates, audit trails, and Slack communication requirements.

## Details

Multi-step process: 1) Obtain written approval from Dr. Sarah Lin (Clinical Review Lead) via email or Slack, 2) Update authorizations table with determination='APPROVED', approval_code='MANUAL-' + timestamp, determined_by='manual-override', and reference documentation in notes field, 3) Log action in #preauth-ops Slack channel with reason and approval reference. This process bypasses normal clinical criteria evaluation and requires explicit clinical leadership authorization for emergency situations.
