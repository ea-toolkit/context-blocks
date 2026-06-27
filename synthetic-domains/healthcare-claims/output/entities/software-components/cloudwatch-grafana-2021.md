---
type: software-component
id: cloudwatch-grafana-2021
name: CloudWatch + Grafana (2021)
description: |-
  Original monitoring setup using CloudWatch and custom Grafana dashboards, replaced by Datadog in Q3 2022
status: deprecated
tags:
- legacy-era
- monitoring
- replaced
source_documents:
- original-architecture-2021.txt
confidence: 0.9
superseded_by:
- datadog
---

# CloudWatch + Grafana (2021)

## Overview

The 2021 monitoring solution combined CloudWatch for metrics collection with custom Grafana dashboards for visualization. This was later replaced by Datadog in Q3 2022 for better observability.

## Details

The original monitoring infrastructure used AWS CloudWatch for metrics collection paired with custom-built Grafana dashboards for visualization and alerting. This combination provided basic observability for the new microservices architecture but was later replaced by Datadog in Q3 2022, likely for better service monitoring capabilities, integrated APM, and reduced operational overhead of maintaining custom dashboards. The timing suggests this upgrade happened after the initial migration stabilized and the team could focus on operational improvements.
