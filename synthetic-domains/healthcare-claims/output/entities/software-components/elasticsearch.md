---
type: software-component
id: elasticsearch
name: Elasticsearch
description: Search engine powering provider search functionality in the Member Portal
status: active
tags:
- search-engine
- provider-search
- indexing
source_documents:
- architecture-overview.txt
confidence: 0.95
used_by:
- provider-directory
consumed_by:
- member-portal
---

# Elasticsearch

## Overview

Elasticsearch provides the search capabilities for the Provider Directory, enabling members to search for healthcare providers through the Member Portal. It indexes provider data to support fast, flexible provider searches with filtering by network status and other criteria.

## Details

Used specifically for provider search functionality exposed via the Member Portal. Indexes provider data from the Provider Directory including demographics, specialties, locations, and network participation status. Enables members to quickly find in-network providers based on various search criteria such as location, specialty, and network status. The search results are filtered by network status per the member's specific plan.
