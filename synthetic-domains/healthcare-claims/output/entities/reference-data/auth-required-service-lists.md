---
type: reference-data
id: auth-required-service-lists
name: Auth-Required Service Lists
description: |-
  Lists of medical services that require prior authorization, maintained per benefit plan
status: active
tags:
- prior-authorization
- benefit-plans
- quarterly-updates
source_documents:
- architecture-overview.txt
confidence: 0.85
used_by:
- claims-gateway
- rules-engine
owned_by:
- claims-operations
---

# Auth-Required Service Lists

## Overview

Auth-required service lists define which medical services require prior authorization approval before they can be covered. These lists are maintained per benefit plan and updated quarterly to reflect changing clinical policies and cost management strategies.

## Details

Maintained per benefit plan since different plans may have different authorization requirements based on their design and cost management approach. Updated quarterly to reflect changes in clinical guidelines, cost management strategies, and regulatory requirements. Used by both the Claims Gateway during intake (to route claims for auth-required services to Pre-Auth Service) and the Rules Engine during adjudication (to deny claims lacking required authorization). The lists typically include high-cost procedures, specialty services, and services with high potential for overutilization.
