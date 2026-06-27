---
type: reference-data
id: clearview-hardened-base-images
name: Clearview Hardened Base Images
description: Security-hardened container base images stored in Google Artifact Registry
status: active
tags:
- infrastructure
- security
- container-images
source_documents:
- claims-coding-standards.txt
confidence: 1.0
used_by:
- claims-gateway
- fraud-detection
---

# Clearview Hardened Base Images

## Overview

Custom security-hardened container base images maintained by Clearview and stored in Google Artifact Registry. Provides standardized, secure foundation for all containerized services with consistent security configurations.

## Details

Clearview maintains its own hardened container base images stored in gcr.io/clearview-prod/base-java:17 and other variants in Google Artifact Registry. These images provide security-hardened foundations for containerized services, ensuring consistent security configurations, minimal attack surface, and controlled software supply chain. All services must use these standardized base images rather than public images to maintain security standards and compliance requirements.
