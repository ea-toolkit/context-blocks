---
type: jargon-tech
id: healthlogic-sdk
name: HealthLogic SDK
description: Vendor software development kit for integrating with HealthLogic Rules
  Engine
status: active
tags:
- vendor-integration
- rules-engine
- dependency-management
source_documents:
- claims-coding-standards.txt
confidence: 1.0
integrates_with:
- rules-engine
---

# HealthLogic SDK

## Overview

Software development kit provided by the HealthLogic vendor for integrating with their rules engine. Pinned to exact versions rather than version ranges to ensure consistent behavior and avoid unexpected changes.

## Details

The HealthLogic SDK enables integration between Clearview's services and the HealthLogic Rules Engine used for claims adjudication. The SDK is pinned to exact versions (not ranges) as part of the dependency management standards to ensure predictable behavior and avoid issues from automatic updates. This reflects the critical nature of the rules engine integration and the need for controlled updates to prevent adjudication logic changes without explicit review.
