---
type: platform
id: google-cloud-platform
name: Google Cloud Platform
description: Cloud infrastructure platform hosting OCR pipeline components and storage
status: active
tags:
- cloud-platform
- infrastructure
source_documents:
- ocr-pipeline-extracted-spec.txt
confidence: 0.85
used_by:
- ocr-pipeline
enables:
- google-document-ai
---

# Google Cloud Platform

## Overview

GCP provides the hosting environment for the OCR pipeline including GKE clusters for the Python application and GCS buckets for image storage. Also hosts the Google Document AI service used for OCR extraction.

## Details

Hosts the OCR pipeline Python 3.9 application in GKE claims-ops namespace and provides GCS bucket gs://clearview-claims-scans/ for storing original scanned images with 7-year retention requirement. The platform also provides the Google Document AI API service used for actual OCR processing at $0.02 per page.
