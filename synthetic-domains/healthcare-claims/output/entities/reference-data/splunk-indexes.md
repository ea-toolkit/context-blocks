---
type: reference-data
id: splunk-indexes
name: Splunk Indexes
description: Service-specific Splunk log indexes with HIPAA-compliant partitioning
status: active
tags:
- observability
- hipaa-compliance
- log-management
source_documents:
- claims-coding-standards.txt
confidence: 1.0
used_by:
- splunk
contains_logs_from:
- pre-auth-service
---

# Splunk Indexes

## Overview

Dedicated Splunk indexes organized by service for log segregation and access control. Includes special HIPAA-compliant index partition for PHI-containing logs from clinical review processes.

## Details

Splunk indexes are organized by service: claims-gateway, rules-engine, payment-engine, eligibility-service, fraud-detection, claims-batch-processing, and preauth-service. The Pre-Auth Service index includes a HIPAA index partition for clinical review logs containing Protected Health Information, which requires special access controls and retention policies. This segregation enables service-specific log analysis while maintaining HIPAA compliance for PHI-containing logs.
