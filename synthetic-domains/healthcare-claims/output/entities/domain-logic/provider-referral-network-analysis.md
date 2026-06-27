---
type: domain-logic
id: provider-referral-network-analysis
name: Provider Referral Network Analysis
description: |-
  Fraud detection model feature to identify coordinated billing patterns between referring providers
status: active
tags:
- fraud-detection
- network-analysis
- in-development
source_documents:
- meeting-notes-quarterly-ops-review-2025q3.txt
confidence: 0.85
enforced_by:
- fraud-detection
---

# Provider Referral Network Analysis

## Overview

Advanced fraud detection capability being developed to identify potential fraud rings by analyzing referral patterns between providers who exclusively refer to each other. Aims to detect coordinated fraudulent billing schemes.

## Details

Sophisticated fraud detection feature under development that analyzes provider referral networks to identify suspicious patterns indicating potential fraud rings. The model looks for providers who refer exclusively to each other, which could indicate coordinated billing schemes rather than legitimate medical referrals based on patient needs and geographic convenience. This represents an evolution from individual claim scoring to network-based fraud pattern detection.
