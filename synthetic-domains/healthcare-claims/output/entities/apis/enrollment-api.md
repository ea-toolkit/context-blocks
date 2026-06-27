---
type: api
id: enrollment-api
name: Enrollment API
description: |-
  Real-time API interface for individual enrollment changes from benefits administration system
status: active
tags:
- real-time
- enrollment
- individual-changes
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.85
exposed_by:
- benefits-administration-system
consumed_by:
- eligibility-service
---

# Enrollment API

## Overview

Real-time API provided by the benefits administration system for processing individual member enrollment changes as they occur, separate from the nightly batch EDI 834 processing.

## Details

One of three enrollment data feeds from the benefits administration system, handling individual enrollment changes in real-time rather than batch. Complements the nightly EDI 834 batch processing for group changes and open enrollment batch loads. Enables immediate enrollment updates for individual member changes without waiting for nightly batch processing.
