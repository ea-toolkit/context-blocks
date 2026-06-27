---
type: process
id: annual-cob-verification-letters
name: Annual COB Verification Letters
description: |-
  Annual mailed letters to verify coordination of benefits information for members with other coverage
status: active
tags:
- traditional-outreach
- low-effectiveness
source_documents:
- eligibility-monitoring-guide.txt
- design-session-cob-handling.txt
confidence: 0.9
owned_by: member-services
validates: cob-data-model
contributes_to: cob-overpayment-incident
complements: cob-questionnaire
---

# Annual COB Verification Letters

## Overview

Annual verification process where letters are mailed to all members with other_coverage = true to verify their coordination of benefits information. Has low response rate of approximately 35%.

## Details

Proactive outreach process to maintain COB data accuracy by mailing verification letters annually to all members flagged as having other coverage (other_coverage = true). Intended to identify changes in other coverage that members haven't reported. Low response rate of ~35% indicates limited effectiveness, contributing to ongoing COB data staleness issues and overpayment risks.

## Open Questions

- Ownership by Member Services is assumed based on member outreach nature, but not explicitly stated

## Additional Details
[from design-session-cob-handling.txt]

Annual outreach campaign using physical mail to request members verify and update their COB information. With only a 35% response rate, this method is even less effective than the portal questionnaire. Combined with the questionnaire's 40% completion rate, these traditional verification methods leave a significant gap in COB data accuracy, necessitating the development of automated detection capabilities.
