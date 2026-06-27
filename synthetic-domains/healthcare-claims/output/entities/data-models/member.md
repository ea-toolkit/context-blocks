---
type: data-model
id: member
name: Member
description: Data model representing health plan members and their enrollment information
status: active
tags:
- core-entity
- pii
- eligibility
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
owned_by:
- eligibility-service
links_to:
- benefit-plan
- accumulator
---

# Member

## Overview

Core member entity stored in Eligibility Service containing demographic information, enrollment status, and benefit plan assignment. Supports subscriber-dependent relationships where one subscriber can have multiple dependents, with historical enrollment tracking for point-in-time coverage validation.

## Details

Format CLV-XXXXXXXXX, stored in Eligibility Service. Contains demographics (name, DOB, gender, address), enrollment details (plan_id, effective/termination dates, enrollment_status: ACTIVE/TERMINATED/COBRA/PENDING), and relationships (subscriber_id for dependents). SSN is stored as SHA-256 hash only. COBRA members have different premium structure but same benefits. Historical enrollment records maintained in member_enrollment_history table with period_start/period_end for retroactive claim processing. HMO plans include PCP assignment via pcp_npi field.
