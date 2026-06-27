---
type: jargon-tech
id: rbrvs
name: RBRVS
description: Resource-Based Relative Value Scale - Medicare's physician payment methodology
status: active
tags:
- medicare
- pricing
- healthcare-standard
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
used_in:
- usual-and-customary
---

# RBRVS

## Overview

Medicare's standardized system for determining physician payment amounts based on the relative value of different medical services. Used as the foundation for calculating usual and customary rates for out-of-network providers.

## Details

Resource-Based Relative Value Scale is Medicare's methodology for physician payments that assigns relative values to medical procedures based on physician work, practice expense, and malpractice costs. In the Clearview context, RBRVS data serves as the baseline for calculating usual and customary rates when no contracted fee schedule exists for out-of-network providers. Geographic adjustment factors are applied to the RBRVS rates to account for regional cost differences.
