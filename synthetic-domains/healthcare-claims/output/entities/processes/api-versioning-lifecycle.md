---
type: process
id: api-versioning-lifecycle
name: API Versioning Lifecycle
description: Platform process for managing API version transitions and deprecation
  timelines
status: active
tags:
- api-management
- versioning
- deprecation-policy
source_documents:
- claims-coding-standards.txt
confidence: 0.9
applies_to:
- claims-submission-api-v2
- eligibility-api-v2
---

# API Versioning Lifecycle

## Overview

Standardized process governing how APIs evolve through major versions, including deprecation notices, support timelines, and breaking change management. Ensures backward compatibility during transitions while enabling API evolution.

## Details

The API versioning lifecycle mandates that major version bumps only occur for breaking changes, with URL path versioning (e.g., /v1/claims, /v2/eligibility) used to distinguish versions. Old versions must be supported for a minimum of 6 months after deprecation notice is issued, providing consumers adequate time to migrate. Current examples include Claims Submission API v1 (deprecated) transitioning to v2 (current), and Eligibility API maintaining v2 as the current version. The process balances innovation with stability for downstream consumers.
