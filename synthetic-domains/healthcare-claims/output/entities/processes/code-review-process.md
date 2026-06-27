---
type: process
id: code-review-process
name: Code Review Process
description: |-
  Mandatory peer review process with coverage, security, and compatibility requirements
status: active
tags:
- development-process
- quality-assurance
- compliance
source_documents:
- claims-coding-standards.txt
confidence: 1.0
applies_to:
- claims-gateway
- eligibility-service
uses:
- confluent-schema-registry
---

# Code Review Process

## Overview

Comprehensive code review process requiring team approval, automated checks, and documentation updates. Ensures code quality, security compliance, and system compatibility before changes reach production.

## Details

Every pull request requires at least one approving review from a team member plus passing all CI checks (build, test, lint, security scan). Code coverage cannot decrease below the 80% line coverage minimum. API changes must include updated OpenAPI specifications, database schema changes require Flyway migration scripts for Java services, and Kafka schema changes must pass Schema Registry compatibility checks. PR descriptions must include change rationale, JIRA ticket reference, testing instructions, and any deployment dependencies such as service deployment order.
