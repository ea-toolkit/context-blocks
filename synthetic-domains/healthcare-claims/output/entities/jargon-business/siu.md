---
type: jargon-business
id: siu
name: SIU
description: |-
  Special Investigation Unit responsible for investigating potential fraud, waste, and abuse cases
status: active
tags:
- fraud-investigation
- manual-review
- compliance
source_documents:
- architecture-overview.txt
confidence: 0.9
related_to:
- fraud-detection
---

# SIU

## Overview

SIU (Special Investigation Unit) is the team responsible for investigating claims flagged for potential fraud, waste, and abuse. They manually review high-scoring claims and investigate suspicious patterns identified by the fraud detection system.

## Details

The specialized investigation team that handles fraud detection alerts. Claims scoring >0.82 on the fraud model are automatically held for SIU review rather than proceeding to adjudication. The SIU also investigates post-payment analysis alerts that identify suspicious patterns like aberrant billing, upcoding, unbundling, or phantom billing. They conduct manual investigations, coordinate with providers, and determine whether suspected fraud cases should be referred to law enforcement or regulatory authorities.
