---
type: external-party
id: unnamed-provider-group
name: Unnamed Provider Group
description: |-
  Provider organization still using Claims Submission API v1 for direct REST submissions
status: active
tags:
- migration-blocker
- direct-submission
source_documents:
- claims-gateway-api-v1-deprecated.txt
confidence: 0.8
consumes:
- claims-submission-api-v1
contact_assigned_to:
- james-whitfield
---

# Unnamed Provider Group

## Overview

An unidentified provider group that submits claims directly via REST API instead of through a clearinghouse, still using the deprecated Claims Submission API v1. James Whitfield was assigned to reach out to them for migration assistance.

## Details

One of only two remaining consumers of the deprecated Claims Submission API v1 as of January 2025. Unlike most providers who submit through clearinghouses, this group submits directly to Clearview's REST API. Their continued use of v1 is blocking the API decommission scheduled for June 2025. James Whitfield from Provider Network team was supposed to contact them for migration support, but their current status is unclear from the documentation.

## Open Questions

- Their current status is unclear from the documentation
