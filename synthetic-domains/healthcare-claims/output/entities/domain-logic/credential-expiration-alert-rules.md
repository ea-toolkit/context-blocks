---
type: domain-logic
id: credential-expiration-alert-rules
name: Credential Expiration Alert Rules
description: |-
  Business rule requiring 90-day advance alerts for credential expiration per NCQA requirements
status: active
tags:
- ncqa-compliance
- automated-alerts
- credentialing
source_documents:
- requirements-provider-portal-2023.txt
confidence: 0.9
enforced_by:
- provider-portal
applies_to:
- credentialing-status-model
---

# Credential Expiration Alert Rules

## Overview

Automated alert system that notifies providers 90 days before credential expiration to ensure compliance with NCQA requirements for 3-year re-credentialing cycles. This rule supports proactive credential management and regulatory compliance.

## Details

The system must alert providers 90 days before credential expiration to comply with NCQA requirements for re-credentialing every 3 years. This includes medical licenses, DEA certificates, malpractice insurance, board certifications, and CME records. The alert system would be automated and integrated with the credentialing status tracking to ensure providers have adequate time to renew credentials before expiration.
