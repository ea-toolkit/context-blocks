---
type: data-model
id: eligibility-response
name: Eligibility Response
description: |-
  Data structure returned by eligibility endpoints containing member status, plan details, and optional accumulator/COB data
status: active
tags:
- api-contract
- response-model
source_documents:
- eligibility-api-reference.txt
confidence: 0.9
used_by:
- eligibility-api-v2
contains:
- member
- accumulator
---

# Eligibility Response

## Overview

Standardized response format used across all eligibility endpoints, containing member_id, status (active/terminated), plan assignment details, effective/termination dates, subscriber relationship, and optional accumulators and coordination of benefits data based on request parameters.

## Details

The response model includes core fields: member_id (CLV-XXXXXXXXX format), status enum, plan_id, plan_name, effective_date, termination_date (null if active), subscriber_id, and relationship. Optional sections include accumulators object with individual/family deductible and OOP max limits/met/remaining amounts, and cob field for coordination of benefits data. The accumulators section also includes pending_reservations array showing active soft reservations with claim_id, reserved_amount, accumulator type, and reserved_at timestamp. Error responses follow a consistent format with error code and message fields.
