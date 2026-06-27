---
type: api
id: claims-submission-api-v2
name: Claims Submission API v2
description: Current version of Claims Submission API with improved design over deprecated
  v1
status: active
tags:
- api
- claims-processing
- current-version
source_documents:
- claims-coding-standards.txt
confidence: 0.8
supersedes:
- claims-submission-api
exposed_by:
- claims-gateway
---

# Claims Submission API v2

## Overview

The current version of the Claims Submission API, representing an evolution from the deprecated v1 implementation. Follows the platform's REST API standards including proper HTTP methods, status codes, and JSON response formats.

## Details

Claims Submission API v2 serves as the current interface for claim submission operations, replacing the deprecated v1 version. Implements the platform's standardized REST conventions including plural resource naming (/claims), proper HTTP status codes (200, 201, 400, 409, etc.), and structured error responses with correlation IDs. Supports both EDI X12 format for traditional clearinghouse submissions and JSON for modern portal-based submissions. The v1 version remains supported for 6 months minimum after deprecation notice per platform policy.

## Open Questions

- Claims Gateway likely exposes the claims submission endpoints
