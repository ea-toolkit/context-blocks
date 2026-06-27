---
type: process
id: eligibility-service-monitoring
name: Eligibility Service Monitoring
description: |-
  Daily operational monitoring process for Eligibility Service metrics and health indicators
status: active
tags:
- monitoring
- operations
- member-services
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.9
owned_by:
- member-services
monitors:
- eligibility-service
depends_on:
- claims-gateway
uses:
- datadog
---

# Eligibility Service Monitoring

## Overview

Member Services engineers monitor key Eligibility Service metrics daily including query rates, accumulator updates, retroactive reprocessing triggers, and cache hit rates. Peak query rate should be ~2,500 req/sec during 10 AM - 3 PM ET business hours.

## Details

Monitoring covers four key metrics via Datadog dashboard 'Eligibility Service — Production': Query rate (~2,500 req/sec peak, alert if <1,000 during peak indicating upstream Claims Gateway issues), accumulator update rate (should track adjudication volume, consumer lag if updates stop), retroactive reprocessing triggers (normal 5-15/day, investigate if >50), and point-in-time query cache hit rate (should be >85%, tune cache if drops). This is separate from Claims Ops broader pipeline monitoring.
