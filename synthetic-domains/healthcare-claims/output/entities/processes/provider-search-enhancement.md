---
type: process
id: provider-search-enhancement
name: Provider Search Enhancement Process
description: |-
  Enhancement of provider search with accepting new patients filter and future distance-based search capability
status: planned
tags:
- member-portal
- november-launch
- provider-directory
source_documents:
- meeting-notes-member-portal-redesign.txt
confidence: 0.8
executed_by:
- member-portal
depends_on:
- provider-directory
uses:
- elasticsearch
---

# Provider Search Enhancement Process

## Overview

Process to improve provider search functionality by adding an 'accepting new patients' filter using existing Provider Directory data. Distance-based search was considered but descoped from November launch due to geocoding requirements.

## Details

The enhancement adds filtering capability to show only providers accepting new patients, utilizing data already available in the Provider Directory system. Distance-based search functionality (within X miles) was discussed but requires geocoding capabilities and latitude/longitude coordinates on provider locations, which would need development by the Provider Network team. For the November launch, the current zip code-based search remains, with distance search moved to the backlog for future implementation.

## Open Questions

- Distance-based search might need geocoding capabilities
