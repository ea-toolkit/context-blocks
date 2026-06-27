---
type: domain-logic
id: pre-authorization-requirements
name: Pre-Authorization Requirements
description: |-
  Service-specific authorization rules maintained per benefit plan and updated quarterly
status: active
tags:
- medical-policy
- cost-control
- quarterly-updates
source_documents:
- claims-processing-workflow.txt
confidence: 0.9
enforced_by:
- pre-auth-service
derives_from:
- auth-required-service-lists
applies_to:
- benefit-plan
---

# Pre-Authorization Requirements

## Overview

Business rules determining which services require prior authorization before claims can be processed. Requirements vary by benefit plan and are updated quarterly to reflect changing medical policies.

## Details

The pre-authorization system maintains service lists that specify which procedures or treatments require prior approval before claims processing. These lists are benefit-plan-specific, meaning different insurance products may have different authorization requirements. The lists are updated quarterly to reflect changes in medical policy, cost management strategies, and regulatory requirements. Services typically requiring authorization include surgeries, certain imaging procedures, specialty drugs, and high-cost treatments, while routine services like office visits rarely require authorization. Claims for auth-required services are denied at intake if no valid authorization exists.
