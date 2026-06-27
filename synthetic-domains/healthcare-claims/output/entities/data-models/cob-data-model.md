---
type: data-model
id: cob-data-model
name: COB Data Model
description: |-
  Data structure storing coordination of benefits information within member records
status: active
tags:
- coordination-of-benefits
- member-data
- payer-tracking
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.95
part_of:
- member
governed_by:
- cob-payer-order-rules
updated_by:
- cob-questionnaire
---

# COB Data Model

## Overview

Data model embedded within member records that tracks coordination of benefits information including other coverage details, payer order, and effective dates for members with multiple health plan coverage.

## Details

Stored within member record with fields: other_coverage (boolean flag), other_payer_id and other_payer_name (identifying secondary payer), payer_order (PRIMARY, SECONDARY, TERTIARY enumeration), other_payer_effective_date and other_payer_termination_date (coverage period tracking). Data often stale as members don't promptly report changes in other coverage, leading to overpayment risk when wrong COB data causes paying as primary when actually secondary.
