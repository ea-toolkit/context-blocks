---
type: data-model
id: benefit-plan
name: Benefit Plan
description: Data model defining member benefit plan configurations and coverage parameters
status: active
tags:
- configuration
- benefits
- cached
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
owned_by:
- eligibility-service
used_by:
- rules-engine
links_to:
- auth-required-service-lists
---

# Benefit Plan

## Overview

Plan configuration data stored in Eligibility Service defining deductibles, copays, coinsurance rates, and coverage rules. Plans are identified by format TIER-TYPE-YEAR (e.g., GOLD-PPO-2025) with different parameters for in-network vs out-of-network services, including prescription drug tiers.

## Details

Stored in benefit_plans table in Eligibility Service. Contains plan identification (plan_id format TIER-TYPE-YEAR, plan_type: PPO/HMO/EPO/POS), financial parameters (individual/family deductibles and OOP max, copays for PCP/specialist/ER visits, in-network and OON coinsurance rates), prescription drug coverage (tier 1-3 copays, tier 4 coinsurance for specialty drugs). Additional configuration includes auth-required service lists (quarterly updates), covered service lists with exclusions, age/sex-specific rules, and COB rules for dual coverage. Rules Engine loads plan config at adjudication start with 15-minute cache TTL for configuration changes.

## Open Questions

- Rules Engine loads plan configuration at the start of adjudication
