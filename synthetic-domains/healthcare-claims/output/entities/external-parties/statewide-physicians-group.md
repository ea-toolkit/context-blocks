---
type: external-party
id: statewide-physicians-group
name: Statewide Physicians Group
description: |-
  Provider group whose fee schedule correction triggered the bulk reprocessing that led to the 2023 payment corruption incident
status: active
tags:
- provider
- contract-related
source_documents:
- postmortem-2023-payment-file-corruption.txt
confidence: 0.85
has_contract_with:
- clearview-health-plans
affected_by:
- inc-2023-0031
---

# Statewide Physicians Group

## Overview

A provider organization under contract with Clearview that required a fee schedule correction in April 2023. The bulk reprocessing of 3,200 claims related to their contract generated the void/reissue operations that triggered the payment corruption incident.

## Details

Statewide Physicians Group had a contract with fee schedule issues that required correction, leading Claims Ops to initiate bulk reprocessing of 3,200 claims on April 27, 2023. This reprocessing generated approximately 800 void/reissue payment operations that ran concurrently with the nightly payment cycle, causing the race condition. The incident resulted in reputational damage with this provider group, as they were both the trigger for the correction and affected by the subsequent financial chaos.
