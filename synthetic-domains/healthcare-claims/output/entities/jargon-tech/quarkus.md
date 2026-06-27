---
type: jargon-tech
id: quarkus
name: Quarkus
description: |-
  Java framework used specifically for Eligibility Service due to superior cold start performance
status: active
tags:
- infrastructure
- java-framework
- performance-optimized
source_documents:
- claims-coding-standards.txt
confidence: 1.0
used_by:
- eligibility-service
---

# Quarkus

## Overview

Cloud-native Java framework optimized for containers and Kubernetes deployments. Selected specifically for Eligibility Service because of its faster startup times, which handle cold starts better on GKE compared to Spring Boot.

## Details

Quarkus was chosen specifically for the Eligibility Service due to its superior cold start performance characteristics on Google Kubernetes Engine. Unlike Spring Boot which is used for other Java services, Quarkus provides faster application startup times and lower memory footprint, making it ideal for services that need to handle dynamic scaling and pod restarts efficiently. This architectural decision reflects performance optimization for the critical eligibility verification workflows.
