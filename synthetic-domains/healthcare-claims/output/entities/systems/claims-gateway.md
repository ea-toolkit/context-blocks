---
type: system
id: claims-gateway
name: Claims Gateway
description: |-
  System that receives all incoming claims, validates format, checks duplicates, and routes downstream
status: active
tags:
- seed-context-derived
- foundation
source_documents:
- seed-context
confidence: 0.9
owned_by:
- claims-operations
---

# Claims Gateway

## Overview

Claims Gateway is the entry point for all claims submission types including EDI 837 files from clearinghouses, JSON submissions from portal, and OCR-processed paper claims. It handles initial validation and routing.

## Details

The Claims Gateway validates incoming claim formats, performs duplicate checking, and routes validated claims to downstream systems for processing. When people refer to 'the gateway is backed up' they mean this system is experiencing processing delays.
