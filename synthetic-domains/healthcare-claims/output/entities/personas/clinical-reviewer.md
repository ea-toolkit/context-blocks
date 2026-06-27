---
type: persona
id: clinical-reviewer
name: Clinical Reviewer
description: |-
  Internal staff persona who reviews pended claims and pre-authorization requests requiring clinical evaluation
status: active
tags:
- internal-user
- clinical-workflow
- tooling-improvement
source_documents:
- meeting-notes-member-portal-redesign.txt
confidence: 0.9
uses:
- manual-data-entry-tool
served_by:
- claims-operations
initiates:
- manual-auth-override
---

# Clinical Reviewer

## Overview

Clinical reviewers evaluate claims that require manual review and pre-authorization requests that cannot be auto-approved. They currently use basic database query tools but need improved workflow interfaces for efficient claim review.

## Details

Clinical reviewers are internal Clearview staff responsible for evaluating claims pended for manual review and pre-authorization requests requiring clinical judgment. They currently work with an internal tool described as 'database queries wrapped in a web form' which lacks proper workflow capabilities. The persona is requesting improved tooling that would show claim details, member history, clinical criteria, and provide an approve/deny workflow interface. This improvement project is planned for Q1 2026 and would utilize similar backend APIs as the member-facing portal but with different user interface requirements focused on clinical decision-making workflows.
