---
type: jargon-business
id: usual-and-customary
name: Usual and Customary
description: Pricing methodology for out-of-network providers based on Medicare RBRVS
  data
status: active
tags:
- oon
- pricing
- medicare-based
source_documents:
- claims-data-model-reference.txt
confidence: 0.9
used_by:
- rules-engine
alternative_to:
- fee-schedule
---

# Usual and Customary

## Overview

Rate calculation method used for out-of-network providers who don't have contracted fee schedules. Derived from Medicare Resource-Based Relative Value Scale (RBRVS) data with geographic adjustment factors to determine reasonable payment amounts.

## Details

Alternative to contracted fee schedules used when providers are out-of-network and no negotiated rates exist. The calculation uses Medicare RBRVS (Resource-Based Relative Value Scale) as the foundation, then applies geographic adjustment factors to account for regional cost variations. This provides a standardized method for determining 'reasonable' payment amounts for services when no contract exists, helping prevent both underpayment and overpayment scenarios.
