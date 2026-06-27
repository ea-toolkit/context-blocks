---
type: system
id: claimspro
name: ClaimsPro
description: |-
  Legacy .NET monolithic claims processing system replaced during 2020-2021 migration
status: deprecated
tags:
- legacy-era
- monolithic
- replaced
- vendor-product
source_documents:
- original-architecture-2021.txt
confidence: 0.95
superseded_by:
- claims-gateway
- eligibility-service
- payment-engine
- provider-directory
---

# ClaimsPro

## Overview

ClaimsPro was Clearview's original monolithic claims processing system that ran from 2014 to 2021. It was a .NET application running on on-premises Windows servers that handled all claims processing functions in a single application.

## Details

ClaimsPro was a comprehensive monolithic system from ClaimsPro Inc. that included intake, adjudication, eligibility, payment, and provider directory modules. By 2020, it was struggling with scale issues as membership grew from ~500K to projected 800K members. The vendor had effectively stopped development, making it unsustainable. The system's tightly coupled architecture made extraction difficult, particularly for the payment module which was deeply entangled with adjudication logic. Provider data within ClaimsPro was particularly messy, with no clear separation between demographics, credentialing, and contracting data. The monolith shared a single database across all modules, which created data quality and scaling challenges.
