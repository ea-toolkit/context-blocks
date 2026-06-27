---
type: software-component
id: drools
name: Drools
description: Rules execution engine that will power the new custom adjudication system
status: active
tags:
- open-source
- rules-engine
source_documents:
- meeting-notes-vendor-migration-kickoff.txt
confidence: 0.95
used_by:
- drools-rules-engine
---

# Drools

## Overview

Open-source business rules management system that will serve as the core rules execution layer for the new claims adjudication engine. Rules will be authored in DRL (Drools Rule Language) format and version-controlled in Git.

## Details

Drools provides the rules execution framework for the new adjudication system, allowing rules to be written in DRL format and maintained by engineers. This eliminates the dependency on vendor professional services for rule changes. The team needs to benchmark Drools performance with approximately 4,000 rules loaded to ensure it meets processing requirements. Rules will be version-controlled in Git, enabling faster deployment cycles compared to the current HealthLogic system.
