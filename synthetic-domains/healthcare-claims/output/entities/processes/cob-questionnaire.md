---
type: process
id: cob-questionnaire
name: COB Questionnaire
description: |-
  Member Portal questionnaire for collecting coordination of benefits information with ~40% completion rate
status: active
tags:
- member-self-service
- low-effectiveness
source_documents:
- eligibility-monitoring-guide.txt
- design-session-cob-handling.txt
confidence: 0.9
updates: cob-data-model
owned_by: member-services
hosted_on: member-portal
part_of: member-portal
contributes_to: cob-overpayment-incident
---

# COB Questionnaire

## Overview

Online questionnaire on the Member Portal designed to collect coordination of benefits information from members about other health coverage. Has low completion rate of approximately 40%.

## Details

Member-facing questionnaire available through the Member Portal to collect COB information about other health coverage. Critical for maintaining accurate payer order and preventing overpayments, but suffers from low member engagement with only ~40% completion rate. Many members ignore the questionnaire, leading to stale COB data and increased overpayment risk when Clearview pays as primary while actually being secondary payer.

## Additional Details
[from design-session-cob-handling.txt]

Self-service questionnaire available on the member portal where members can report other insurance coverage. Despite being the primary method for COB data collection, it has proven inadequate with only 40% of members completing it. This low completion rate is a key factor in the 30-40% of members having stale COB information, leading to incorrect payer order determination and overpayments.

## Conflicts

⚠️ Description differs: existing says 'Member Portal questionnaire for collecting coordination of benefits information with ~40% completion rate', [design-session-cob-handling.txt] says 'Portal-based questionnaire for members to self-report other insurance coverage'

