---
type: domain-logic
id: hipaa-compliance-requirements
name: HIPAA Compliance Requirements
description: |-
  Comprehensive healthcare data protection requirements covering encryption, access control, and retention
status: active
tags:
- security
- hipaa-compliance
- data-protection
- regulatory
source_documents:
- claims-coding-standards.txt
confidence: 1.0
enforced_by:
- cloud-sql-postgresql
applies_to:
- member-portal
---

# HIPAA Compliance Requirements

## Overview

Comprehensive HIPAA compliance framework covering data encryption, access controls, audit logging, and retention policies. Mandatory for all healthcare data handling with specific technical requirements for PHI protection.

## Details

HIPAA compliance encompasses: no PHI in plaintext logs, all data at rest encrypted (Cloud SQL, GCS), all data in transit encrypted (TLS 1.3 minimum), member SSN stored as SHA-256 hash only, OAuth 2.0 authentication for all endpoints, member-scoped access enforcement for member-facing APIs, audit logging for all member record access, and 7-year data retention per state regulations (using longest requirement across states). These requirements are non-negotiable and violations are detected by CI security scans.
