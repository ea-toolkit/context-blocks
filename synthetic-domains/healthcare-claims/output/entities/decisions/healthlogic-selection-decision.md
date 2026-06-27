---
type: decision
id: healthlogic-selection-decision
name: HealthLogic Selection Decision
description: |-
  Decision to choose HealthLogic Adjudicator over alternatives for rules engine in 2019
status: active
tags:
- legacy-era
- vendor-selection
- regrettable
source_documents:
- original-architecture-2021.txt
confidence: 0.95
applies_to:
- rules-engine
superseded_by:
- adr-2024-007
---

# HealthLogic Selection Decision

## Overview

In 2019, Clearview evaluated three options for their rules engine: HealthLogic, Facets (TriZetto), and building their own. They chose HealthLogic for fastest time-to-market, though this later proved problematic.

## Details

The evaluation considered HealthLogic Adjudicator, Facets from TriZetto, and building a custom solution in-house. HealthLogic was selected because it offered the fastest implementation timeline at 4 months versus 18 months for building their own. However, the document notes this was 'a mistake' in hindsight, with ADR-2024-007 documenting the issues that led to the current replacement effort. The decision prioritized speed over long-term flexibility and control.
