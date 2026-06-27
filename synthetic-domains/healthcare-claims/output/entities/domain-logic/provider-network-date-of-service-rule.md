---
type: domain-logic
id: provider-network-date-of-service-rule
name: Provider Network Date of Service Rule
description: Rule applying provider network status as of service date, not processing
  date
status: active
tags:
- provider-protection
- member-protection
- temporal-logic
source_documents:
- claims-processing-workflow.txt
confidence: 0.9
enforced_by:
- rules-engine
uses:
- provider-directory
applies_to:
- provider
---

# Provider Network Date of Service Rule

## Overview

Business rule that protects both members and providers by applying the provider's network status and contract terms that were effective on the date of service, regardless of when the claim is processed.

## Details

When a provider's network status changes (joins or leaves the network, contract modifications), the rules engine evaluates network status based on the date of service, not the claim processing date. This rule protects both parties: members receive the benefit level they were entitled to when the service was rendered, and providers receive payment under the contract terms that were in effect when they provided the service. For example, if a provider left the network on March 15th but provided services on March 10th, those services are still processed under in-network terms and rates. This prevents retroactive application of network changes that could unfairly impact either members or providers.
