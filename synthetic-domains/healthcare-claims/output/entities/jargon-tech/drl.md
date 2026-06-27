---
type: jargon-tech
id: drl
name: DRL
description: |-
  Drools Rule Language - the format for authoring rules in the new custom rules engine
status: active
tags:
- drools
- rule-authoring
source_documents:
- meeting-notes-vendor-migration-kickoff.txt
confidence: 0.9
used_in:
- drools-rules-engine
applies_to:
- drools
---

# DRL

## Overview

DRL (Drools Rule Language) is the format used to author business rules in the Drools rules engine. Initially, engineers will author rules in DRL format, with clinical teams potentially getting a more user-friendly interface later.

## Details

DRL is the native rule authoring language for Drools, allowing complex business logic to be expressed in a domain-specific language. For the HealthLogic migration, rules will initially be written in DRL by engineers and version-controlled in Git. Rachel noted that clinical teams typically dislike DRL and prefer business-readable formats, suggesting a rule authoring UI or DSL may be needed in later phases. The advantage of DRL is that it eliminates dependency on vendor professional services for rule deployment, enabling faster release cycles.
