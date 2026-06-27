---
type: data-model
id: provider
name: Provider
description: |-
  Data model representing healthcare providers with credentials and network participation
status: active
tags:
- master-data
- credentialing
- network
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
owned_by:
- provider-directory
links_to:
- fee-schedule
used_by:
- rules-engine
---

# Provider

## Overview

Provider master data stored in Provider Directory, keyed by NPI with credentialing information, specialty codes, and network participation status. Supports both individual and organizational providers with location management and contract-based fee schedules.

## Details

National Provider Identifier (NPI) as primary key, stored in Provider Directory. Contains provider type (1=Individual, 2=Organization), demographics/org name, specialty taxonomy codes, credentials (MD, DO, NP, PA), licensing information with expiration tracking. Credentialing status (ACTIVE/PENDING/EXPIRED/REVOKED) with 3-year NCQA re-credentialing cycle. Network participation tracked per plan via provider_network_status table (IN_NETWORK/OUT_OF_NETWORK/PENDING) with effective dates. Multiple locations supported via provider_locations table. Fee schedules linked via contract_id for allowed amount calculations during adjudication.
