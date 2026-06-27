---
type: system
id: drools-rules-engine
name: Drools-Based Rules Engine
description: |-
  New custom claims adjudication engine being built to replace HealthLogic Adjudicator
status: planned
tags:
- migration-target
- spring-boot
- drools
source_documents:
- meeting-notes-vendor-migration-kickoff.txt
confidence: 0.9
supersedes:
- healthlogic-adjudicator
owned_by:
- claims-operations
depends_on:
- drools
- drg-grouper-library
---

# Drools-Based Rules Engine

## Overview

A Java-based Spring Boot service using Drools for rule execution, designed to replace HealthLogic Adjudicator. The system will handle the same ~4,200 rules but with faster deployment cycles and lower operational costs.

## Details

Built as a Java Spring Boot service using Drools as the rules execution layer. Rules will be authored in DRL files and version-controlled in Git, eliminating dependency on vendor professional services. The migration follows a three-phase approach: Phase 1 (build through Q3 2025), Phase 2 (parallel processing in Q4 2025), and Phase 3 (cutover in Q1 2026). Initially, rules will be engineer-authored in DRL format, with clinical teams potentially getting a UI later. The system must achieve 99.5% disposition match rate and 99.9% payment amount accuracy during parallel testing.
