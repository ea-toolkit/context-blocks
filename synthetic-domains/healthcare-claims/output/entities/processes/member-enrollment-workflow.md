---
type: process
id: member-enrollment-workflow
name: Member Enrollment Workflow
description: |-
  End-to-end process for enrolling members in health plans and managing enrollment changes
status: planned
tags:
- undocumented
- high-priority
- member-facing
source_documents:
- enrollment-workflow.txt
confidence: 0.9
owned_by:
- dana-okafor
executed_by:
- eligibility-service
triggers:
- retroactive-enrollment-reprocessing
---

# Member Enrollment Workflow

## Overview

The comprehensive business process covering how members join Clearview Health Plans, change their coverage, and handle life events that affect their enrollment. This includes both the business workflow steps and technical implementation through the Eligibility Service.

## Details

This process encompasses multiple enrollment scenarios: new member enrollment when someone first joins a plan, open enrollment periods where existing members can change their coverage, qualifying life events (marriage, birth, job change) that allow mid-year changes, COBRA enrollment for members losing employer coverage, and retroactive enrollment changes that require claims reprocessing. The process involves both business workflow management and technical implementation through EDI 834 enrollment file processing in the Eligibility Service. Currently undocumented, causing confusion for new engineers who frequently ask about the enrollment flow.
