---
type: domain-logic
id: eligibility-date-of-service-rule
name: Eligibility Date of Service Rule
description: |-
  Business rule requiring eligibility verification against date of service, not submission date
status: active
tags:
- eligibility-rule
- temporal-logic
source_documents:
- claims-processing-workflow.txt
confidence: 0.95
enforced_by:
- eligibility-service
applies_to:
- claim
---

# Eligibility Date of Service Rule

## Overview

Critical business rule that validates member eligibility based on when the service was rendered, not when the claim was submitted. This protects against coverage gaps and ensures proper benefit application.

## Details

The eligibility verification process must use the date of service from the claim, not the submission date, to determine member coverage status. This rule is essential because claims may be submitted days or weeks after the service was provided, and the member's coverage status could have changed in the interim. For example, a claim submitted 30 days after service must verify the member had active coverage on the original service date. This rule ensures accurate benefit determination and prevents inappropriate denials for services rendered during valid coverage periods.
