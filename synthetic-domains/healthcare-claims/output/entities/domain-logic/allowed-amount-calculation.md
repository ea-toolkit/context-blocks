---
type: domain-logic
id: allowed-amount-calculation
name: Allowed Amount Calculation
description: |-
  Business rule that calculates the maximum payable amount based on provider contract fee schedules
status: active
tags:
- adjudication
- fee-schedule
- payment-calculation
source_documents:
- architecture-overview.txt
confidence: 0.95
enforced_by:
- rules-engine
derives_from:
- provider-directory
---

# Allowed Amount Calculation

## Overview

The allowed amount calculation determines the maximum amount the plan will pay for a service based on the provider's contract fee schedule. This is a critical rule because member cost-sharing is calculated against the allowed amount, not the billed amount.

## Details

Executed during adjudication to determine payment amounts. The allowed amount comes from the provider's contract fee schedule stored in the Provider Directory, not from what the provider billed. This is a common source of confusion for new engineers - providers often bill higher amounts than contracted rates. Member cost-sharing (deductible, copay, coinsurance) is always calculated against the allowed amount. For out-of-network providers, different fee schedule rules apply. The calculation considers the provider's network status as of the claim's date of service, not the processing date.
