---
type: api
id: provider-portal-bff
name: Provider Portal Backend-for-Frontend
description: |-
  Proposed BFF API to serve the Provider Portal frontend with provider-specific data aggregation
status: proposed
tags:
- bff-pattern
- provider-facing
- api-aggregation
source_documents:
- requirements-provider-portal-2023.txt
confidence: 0.8
exposes:
- provider-portal
communicates_with:
- provider-directory
- payment-engine
---

# Provider Portal Backend-for-Frontend

## Overview

A proposed Backend-for-Frontend service that would aggregate data from multiple backend services (Provider Directory, Payment Engine, Pre-Auth Service) to serve the Provider Portal frontend. This architectural approach would separate provider-facing API concerns from internal system APIs.

## Details

James Whitfield prefers building a separate BFF rather than extending the existing Provider Directory API with provider-facing endpoints, to avoid mixing internal and external API concerns. The BFF would handle authentication, authorization, and data aggregation from Provider Directory for profile data, Payment Engine for payment history and ERA 835 access, and potentially Pre-Auth Service for prior authorization submission. The service would implement role-based access control and handle the provider-specific data formatting and security requirements.

## Open Questions

- Could be a new BFF that talks to Provider Directory, Payment Engine, Pre-Auth Service
