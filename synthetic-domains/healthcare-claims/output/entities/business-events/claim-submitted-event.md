---
type: business-event
id: claim-submitted-event
name: Claim Submitted Event
description: Event triggered when a provider submits a claim through any intake channel
status: active
tags:
- claims-processing
- intake
- provider-initiated
source_documents:
- architecture-overview.txt
confidence: 0.9
published_by:
- claims-gateway
triggers:
- duplicate-detection-process
- claim-routing-process
---

# Claim Submitted Event

## Overview

The claim submitted event is generated when healthcare providers submit claims through EDI 837, JSON API, or paper/OCR channels. This event initiates the claims processing workflow and carries the claim data through the validation and routing pipeline.

## Details

Triggered when providers submit claims via EDI 837 Professional/Institutional, JSON REST API, or paper claims through OCR. The event carries the complete claim data including member information, provider details, service dates, procedure codes, and billed amounts. This event initiates the Claims Gateway processing pipeline including format validation, duplicate detection, and downstream routing to eligibility verification, fraud scoring, and adjudication systems.
