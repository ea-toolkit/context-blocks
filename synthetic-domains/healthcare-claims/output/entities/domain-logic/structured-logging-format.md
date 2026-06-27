---
type: domain-logic
id: structured-logging-format
name: Structured Logging Format
description: Mandatory JSON logging format with correlation ID and metadata requirements
status: active
tags:
- observability
- logging-standards
- debugging
source_documents:
- claims-coding-standards.txt
confidence: 1.0
enforced_by:
- splunk
---

# Structured Logging Format

## Overview

Standardized structured JSON logging format required across all services. Includes timestamp, level, service identifier, correlation ID, message, and metadata fields to enable consistent log analysis and debugging.

## Details

All services must log in structured JSON format containing: timestamp (ISO 8601), level (DEBUG/INFO/WARN/ERROR), service name, correlation_id (claim_id for claim operations, auth_id for auth operations), message, and metadata object. Correlation IDs are mandatory for tracing operations across service boundaries. The format enables consistent parsing by Splunk and supports operational debugging through request correlation. Log levels should be used appropriately: DEBUG for detailed processing, INFO for operations, WARN for recoverable issues, ERROR for failures.
