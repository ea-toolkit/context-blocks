---
type: software-component
id: google-cloud-storage
name: Google Cloud Storage
description: Cloud storage service used for ML model binaries and configuration files
status: active
tags:
- storage
- google-cloud
- configuration
source_documents:
- deployment-guide.txt
confidence: 0.85
used_by:
- fraud-detection-deployment
- pre-auth-service-deployment
deployed_on:
- google-cloud-platform
---

# Google Cloud Storage

## Overview

Google Cloud Storage buckets used for storing ML model binaries for Fraud Detection and configuration files for Pre-Auth Service clinical criteria.

## Details

GCS buckets serve multiple purposes: storing fraud detection model binaries that pods pick up on startup, and housing Pre-Auth Service clinical criteria files at gs://clearview-preauth-config/criteria/. This provides a deployment mechanism outside the standard CI/CD pipeline for configuration and model updates.
