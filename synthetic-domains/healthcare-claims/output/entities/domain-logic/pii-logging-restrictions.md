---
type: domain-logic
id: pii-logging-restrictions
name: PII Logging Restrictions
description: HIPAA compliance rules prohibiting Protected Health Information in logs
status: active
tags:
- security
- hipaa-compliance
- pii-protection
source_documents:
- claims-coding-standards.txt
confidence: 1.0
applies_to:
- member
---

# PII Logging Restrictions

## Overview

Strict HIPAA compliance rules prohibiting any Protected Health Information (PHI) from appearing in application logs. Only member IDs and other non-PHI identifiers are permitted, with violations flagged by CI security scans.

## Details

HIPAA compliance requires that PII fields including member name, SSN, and date of birth must NEVER appear in logs. Only member IDs and other non-identifying reference numbers are permitted for correlation and debugging. This rule is enforced by security scans in the CI pipeline that flag potential violations. Violations cannot be bypassed, ensuring consistent HIPAA compliance across all services and preventing accidental PHI exposure in log aggregation systems.
