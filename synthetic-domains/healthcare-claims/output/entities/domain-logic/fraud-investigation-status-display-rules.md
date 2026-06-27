---
type: domain-logic
id: fraud-investigation-status-display-rules
name: Fraud Investigation Status Display Rules
description: |-
  Business rule hiding fraud investigation details from members in portal, showing only 'processing' status
status: active
tags:
- compliance
- member-portal
- fraud-investigation
source_documents:
- meeting-notes-fraud-detection-integration.txt
confidence: 0.9
enforced_by:
- member-portal
applies_to:
- siu-review-process
---

# Fraud Investigation Status Display Rules

## Overview

Compliance-driven rule that prevents members from seeing fraud investigation status in Member Portal. Claims held for SIU review display as 'processing' to avoid alerting potential fraudsters.

## Details

Business rule requiring that claims held for fraud investigation display only generic 'processing' status in Member Portal, never revealing that fraud review is occurring. This compliance requirement prevents potential fraudsters from learning their claims are under investigation, which could lead to altered behavior or destruction of evidence. Rule applies to all fraud-flagged claims regardless of investigation outcome.
