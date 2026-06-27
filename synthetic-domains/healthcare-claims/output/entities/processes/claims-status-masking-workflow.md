---
type: process
id: claims-status-masking-workflow
name: Claims Status Masking Workflow
description: |-
  Business process for displaying appropriate claim status to members while hiding fraud investigation details
status: active
tags:
- compliance
- fraud-detection
- member-experience
source_documents:
- meeting-notes-member-portal-redesign.txt
confidence: 0.9
owned_by:
- member-services
involves:
- compliance-team
executed_by:
- member-portal
---

# Claims Status Masking Workflow

## Overview

Workflow that ensures members see 'Under Review' status for both manual pend and SIU fraud investigation holds, with identical visual treatment and messaging. This protects the integrity of fraud investigations while providing transparency to members.

## Details

The workflow masks sensitive claim statuses to prevent members from knowing their claims are under fraud investigation. Both claims pended for manual review and claims held for SIU investigation display as 'Under Review' with the message 'your claim requires additional review' and no estimated completion time. This compliance-driven requirement ensures fraud investigations remain confidential while still providing members with status information. The workflow applies to all member-facing status displays in the portal redesign.
