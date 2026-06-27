---
type: domain-logic
id: duplicate-detection-logic
name: Duplicate Detection Logic
description: Composite key matching logic to identify duplicate claims within 90-day
  window
status: active
tags:
- validation-rule
- fraud-prevention
source_documents:
- claims-processing-workflow.txt
confidence: 0.9
enforced_by:
- claims-gateway
part_of:
- duplicate-detection-process
---

# Duplicate Detection Logic

## Overview

Business rule that prevents duplicate claim processing by checking composite keys of member ID, provider NPI, date of service, and procedure codes. Uses a 90-day lookback window to identify exact and near-duplicates.

## Details

The duplicate detection algorithm uses a composite key consisting of: member ID + provider NPI + date of service + procedure codes. Claims are checked against this composite key for matches within the last 90 days. Exact duplicates (identical composite keys) are rejected immediately with no further processing. Near-duplicates (matching composite key but different billed amounts for the same service) are flagged and routed to manual review rather than automatic rejection, as these may represent legitimate corrections or appeals.
