---
type: process
id: secure-messaging-claim-context
name: Secure Messaging Claim Context Process
description: |-
  Enhancement to show claim details inline when members message about specific claims
status: proposed
tags:
- member-services
- integration
- third-party
source_documents:
- meeting-notes-member-portal-redesign.txt
confidence: 0.7
depends_on:
- zendesk-integration
involves:
- member-services
uses:
- claim
---

# Secure Messaging Claim Context Process

## Overview

Process to provide Member Services representatives with claim context when members send messages about specific claims. This requires integration with the Zendesk messaging backend to pass claim information through their API.

## Details

The process enhances the existing secure messaging functionality by detecting when member messages relate to specific claims and providing representatives with inline access to those claim details. The implementation requires utilizing Zendesk API capabilities to pass claim context information. Feasibility assessment is needed to determine the technical approach for integrating claim data with the third-party messaging platform. This enhancement aims to improve representative efficiency and member service quality by providing immediate access to relevant claim information during conversations.

## Open Questions

- The messaging service appears to be Zendesk
- This might need backend work on the messaging service
