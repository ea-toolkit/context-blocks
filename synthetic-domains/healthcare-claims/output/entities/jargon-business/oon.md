---
type: jargon-business
id: oon
name: OON
description: Out-of-Network, referring to providers not contracted with the health
  plan
status: active
tags:
- provider-network
- member-reimbursement
- higher-cost-sharing
source_documents:
- architecture-overview.txt
confidence: 0.9
contrasts_with:
- in-network
---

# OON

## Overview

OON (Out-of-Network) refers to healthcare providers who do not have contracts with Clearview Health Plans. Members typically have higher cost-sharing for OON services, and OON claims often require member reimbursement rather than direct provider payment.

## Details

Providers who are not contracted with Clearview Health Plans and therefore not in the plan's provider network. Members using OON providers typically face higher deductibles, coinsurance, or copays. OON claims are often processed as member reimbursements rather than direct provider payments since there's no contractual relationship with the provider. The Member Portal includes OON claim submission functionality, and the payment engine processes OON reimbursements within 10 business days.

## Open Questions

- In-network entity not explicitly defined in this document
