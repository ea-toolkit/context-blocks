---
type: process
id: provider-change-approval-workflow
name: Provider Change Approval Workflow
description: |-
  Two-business-day approval process for provider demographic changes submitted through the portal
status: active
tags:
- approval-workflow
- two-day-sla
- data-quality
source_documents:
- requirements-provider-portal-2023.txt
confidence: 0.85
executed_by:
- provider-portal
involves:
- clearview-provider-relations-rep
---

# Provider Change Approval Workflow

## Overview

A workflow process where Provider Relations Representatives review and approve provider-submitted changes to demographic information within 2 business days. This process ensures data quality while enabling provider self-service for non-critical updates.

## Details

When providers submit changes to address, phone, fax, email, office hours, or accepting-new-patients status through the portal, these changes enter an approval queue for Provider Relations review. The process has a 2-business-day SLA for review and approval. Once approved, changes are pushed to the Provider Directory in real-time. Sensitive changes like NPI, TIN, specialty, and credentials require manual review and cannot be self-updated through the portal.
