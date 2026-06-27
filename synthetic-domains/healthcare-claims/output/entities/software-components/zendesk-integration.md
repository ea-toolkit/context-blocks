---
type: software-component
id: zendesk-integration
name: Zendesk Integration
description: Third-party customer service platform underlying secure messaging functionality
status: active
tags:
- third-party
- messaging
- member-services
source_documents:
- meeting-notes-member-portal-redesign.txt
confidence: 0.8
used_by:
- member-portal
serves:
- member-services
---

# Zendesk Integration

## Overview

Zendesk serves as the backend platform for member secure messaging capabilities in the Member Portal. The integration enables members to communicate with Member Services representatives through the portal interface.

## Details

Zendesk provides the underlying messaging infrastructure for member-to-representative communication within the Member Portal. The platform handles message routing, conversation management, and representative workflow tools. For the secure messaging enhancement, the Zendesk API would need to be utilized to pass claim context information when members message about specific claims. The integration's API capabilities need to be assessed to determine feasibility for the claim context feature.

## Open Questions

- The messaging service is likely Zendesk
