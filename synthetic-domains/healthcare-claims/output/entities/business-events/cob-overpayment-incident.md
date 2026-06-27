---
type: business-event
id: cob-overpayment-incident
name: COB Overpayment Problem
description: Ongoing issue causing $4-6M annual overpayment due to stale COB data
status: active
tags:
- compliance-issue
- financial-impact
source_documents:
- design-session-cob-handling.txt
confidence: 0.95
identified_by:
- compliance-team
drives:
- cob-auto-detection-project
related_to:
- cob
---

# COB Overpayment Problem

## Overview

Systemic problem where 30-40% of members with other coverage have stale COB information, resulting in Clearview paying as primary when they should be secondary.

## Details

Compliance team estimates $4-6M annual overpayment due to incorrect payer order when COB data is outdated. Current verification methods are inadequate: portal COB questionnaire achieves only 40% completion rate, annual verification letters get 35% response rate. This creates ongoing financial exposure and regulatory compliance risk, driving the need for automated COB detection capabilities.
