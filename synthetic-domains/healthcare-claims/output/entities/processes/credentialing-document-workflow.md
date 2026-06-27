---
type: process
id: credentialing-document-workflow
name: Credentialing Document Workflow
description: |-
  Process for providers to upload credentialing documents and specialists to review them
status: active
tags:
- credentialing
- document-management
- ncqa-compliance
source_documents:
- requirements-provider-portal-2023.txt
confidence: 0.9
executed_by:
- provider-portal
involves:
- credentialing-specialist
---

# Credentialing Document Workflow

## Overview

A workflow enabling providers to upload credentialing documents through the portal, with automatic notification to Credentialing Specialists for review. The process tracks credentialing status and provides automated expiration alerts.

## Details

Providers can upload medical licenses, DEA certificates, malpractice insurance, board certifications, and CME records in PDF, JPG, or PNG format (max 10MB per file). Documents are stored in a secure document management system and Credentialing Specialists are automatically notified of new uploads. The system tracks credentialing status (ACTIVE, PENDING, EXPIRED, REVIEW_REQUIRED) and sends alerts 90 days before credential expiration to comply with NCQA requirements for 3-year re-credentialing cycles.
