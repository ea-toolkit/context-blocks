---
type: domain-logic
id: api-error-response-format
name: API Error Response Format
description: Standardized error response structure across all platform APIs
status: active
tags:
- api-standards
- error-handling
- observability
source_documents:
- claims-coding-standards.txt
confidence: 1.0
enforced_by:
- claims-gateway
- eligibility-service
- payment-engine
---

# API Error Response Format

## Overview

Consistent error response format implemented across all claims platform APIs, providing structured error information including machine-readable codes, human descriptions, and correlation tracking for debugging.

## Details

All APIs must return errors in a standardized JSON format containing: error (machine-readable code), message (human-readable description), details (additional context object), and correlation_id (claim-id or request-id for tracing). This format enables consistent error handling across frontend applications and downstream consumers while supporting operational debugging through correlation ID tracking. The structured approach separates user-facing messages from technical details and provides extensible detail objects for context-specific error information.
