---
type: process
id: accumulator-pre-creation-process
name: Open Enrollment Accumulator Pre-Creation
description: |-
  Process to pre-create next plan year accumulators during open enrollment to prevent plan year boundary issues
status: planned
tags:
- plan-year
- enrollment
- prevention
source_documents:
- design-session-accumulator-rework.txt
confidence: 0.9
creates:
- accumulator
part_of:
- open-enrollment-process
prevents:
- november-2024-accumulator-incident
---

# Open Enrollment Accumulator Pre-Creation

## Overview

A planned process change to create accumulators for the upcoming plan year during open enrollment processing rather than relying on batch jobs at the plan year transition. This approach ensures accumulators are ready before January 1st and prevents the type of incident that occurred in November 2024.

## Details

This process will integrate accumulator creation into the existing open enrollment workflow, ensuring that when members enroll or re-enroll for the next plan year, their corresponding accumulators (individual deductible, family deductible, individual OOP, family OOP) are created immediately. This eliminates the dependency on batch jobs running exactly at the plan year boundary and provides a more robust approach to plan year transitions. The process addresses the fragility identified in the November 2024 incident where accumulators weren't available until after the batch job execution, causing disruption to claims processing and member portal displays.
