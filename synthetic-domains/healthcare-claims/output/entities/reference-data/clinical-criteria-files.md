---
type: reference-data
id: clinical-criteria-files
name: Clinical Criteria Files
description: |-
  GCS-stored configuration files defining clinical rules for authorization decisions
status: active
tags:
- configuration
- clinical
- gcs
source_documents:
- pre-auth-runbook.txt
confidence: 0.9
used_by:
- pre-auth-service
---

# Clinical Criteria Files

## Overview

Configuration files stored in Google Cloud Storage that contain the clinical decision rules used by the Pre-Auth Service for automatic authorization approvals and denials.

## Details

Files stored in gs://clearview-preauth-config/criteria/ bucket and loaded by the Pre-Auth Service on startup via CriteriaLoader component. Updates to these files directly impact auto-approval rates and require clinical team coordination. Failed loading triggers 'Failed to load criteria' errors and may require Platform Engineering assistance for GCS access issues. Files are versioned to enable comparison between releases when investigating approval rate changes.
