---
type: business-event
id: enrollment-change-event
name: Enrollment Change Event
description: |-
  Event triggered when member enrollment data is modified, potentially with retroactive effective dates
status: active
tags:
- event-driven
- kafka
- eligibility
source_documents:
- architecture-overview.txt
- integration-patterns-guide.txt
confidence: 0.95
published_by: eligibility-service
triggers: retroactive-reprocessing
consumed_by: claims-gateway
---

# Enrollment Change Event

## Overview

The enrollment change event is generated when member enrollment information is updated in the Eligibility Service. This includes new enrollments, terminations, and benefit plan changes, which may have retroactive effective dates requiring claim reprocessing.

## Details

Published by the Eligibility Service when member enrollment data is modified. The event includes the member ID, previous and new enrollment details, effective dates, and whether the change is retroactive. Retroactive changes within 60 days automatically trigger the retroactive reprocessing workflow to re-adjudicate any claims processed during the affected time period. This ensures claims are paid correctly based on the member's actual coverage at the time of service.

## Additional Details
[from integration-patterns-guide.txt]

Topic: clearview.eligibility.enrollment.changed with 7-day retention (shorter than other events). Partitioned by member_id. Triggers automatic retroactive claim reprocessing when enrollment changes occur within the 60-day lookback window. Critical for handling enrollment corrections and ensuring proper claim adjudication.
