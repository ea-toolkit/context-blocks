---
type: data-model
id: credentialing-status-model
name: Credentialing Status Model
description: Data model representing provider credentialing status with defined status
  values
status: active
tags:
- credentialing
- status-model
- ncqa-compliance
source_documents:
- requirements-provider-portal-2023.txt
confidence: 0.85
used_by:
- provider-portal
---

# Credentialing Status Model

## Overview

A data model that tracks provider credentialing status through defined status values: ACTIVE, PENDING, EXPIRED, and REVIEW_REQUIRED. The model supports the credentialing workflow and compliance monitoring requirements.

## Details

The credentialing status model includes status enumeration (ACTIVE, PENDING, EXPIRED, REVIEW_REQUIRED) and likely includes expiration dates for tracking 90-day alert requirements. The model supports NCQA compliance requirements for 3-year re-credentialing cycles and integrates with the automated alert system for credential expiration notifications.

## Open Questions

- The model likely includes expiration dates for tracking 90-day alert requirements
