---
type: process
id: professional-claims-processing
name: Professional Claims Processing
description: Real-time processing of 837P professional claims with 30-second SLA
status: active
tags:
- real-time-processing
- high-volume
source_documents:
- claims-processing-workflow.txt
confidence: 0.9
uses:
- edi-837-professional
executed_by:
- claims-gateway
---

# Professional Claims Processing

## Overview

Processing flow for professional claims submitted via EDI 837P format (CMS-1500 equivalent). These claims are processed in real-time with a 30-second SLA at intake due to their simpler structure and higher volume.

## Details

Professional claims use the EDI 837P format and represent the majority of claims volume. Unlike institutional claims, they are processed immediately upon receipt rather than in batches. The 30-second SLA applies at the intake level through the Claims Gateway. These claims typically involve office visits, procedures, and other outpatient services that don't require the complex billing structures of institutional claims.
