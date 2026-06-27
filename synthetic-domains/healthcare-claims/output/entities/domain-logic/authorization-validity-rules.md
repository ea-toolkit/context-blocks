---
type: domain-logic
id: authorization-validity-rules
name: Authorization Validity Rules
description: |-
  Business rules defining how long prior authorizations remain valid for different service types
status: active
tags:
- prior-authorization
- validity-periods
- clinical
source_documents:
- architecture-overview.txt
confidence: 0.9
enforced_by:
- pre-auth-service
- rules-engine
---

# Authorization Validity Rules

## Overview

Authorization validity rules establish time limits for how long prior authorization approvals remain valid. Different service types have different validity periods to balance member access with clinical appropriateness.

## Details

Standard authorizations are valid for 90 days from approval date, while surgical authorizations have a shorter 60-day validity period due to the time-sensitive nature of surgical procedures. These rules are enforced during adjudication - if a claim references a service that required authorization but the authorization has expired, the claim is denied. Auth-required service lists are updated quarterly per benefit plan. The system checks authorization status during both gateway intake and rules engine adjudication.
