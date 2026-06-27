---
type: business-event
id: auth-expiration-warning
name: Auth Expiration Warning
description: |-
  Informational alert for authorizations expiring within 7 days without associated claims
status: active
tags:
- monitoring
- alert
- informational
source_documents:
- pre-auth-runbook.txt
confidence: 0.9
involves:
- dana-okafor
---

# Auth Expiration Warning

## Overview

Non-urgent monitoring alert that identifies authorizations approaching expiration (within 7 days) that haven't been used for claims submission. Provides visibility into potentially unused authorizations.

## Details

The PRE-AUTH-EXPIRY alert tracks authorizations nearing their validity expiration without corresponding claims. Alert example: '[PRE-AUTH-EXPIRY] 87 authorizations expiring in next 7 days without associated claims'. Standard authorizations are valid for 90 days, surgical authorizations for 60 days. High counts of expiring surgical auths may indicate delayed surgeries. Alert is informational unless count exceeds 200, at which point Member Services should be notified of potential provider scheduling issues.
