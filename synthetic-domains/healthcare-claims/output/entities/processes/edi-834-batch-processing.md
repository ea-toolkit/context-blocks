---
type: process
id: edi-834-batch-processing
name: EDI 834 Batch Processing
description: |-
  Nightly batch process for processing group enrollment updates from benefits administration system
status: active
tags:
- batch-processing
- enrollment
- nightly
- edi
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.95
processes:
- edi-834
owned_by:
- member-services
triggers:
- retroactive-reprocessing
depends_on:
- benefits-administration-system
---

# EDI 834 Batch Processing

## Overview

Nightly automated process that picks up EDI 834 enrollment files from SFTP at ~02:00 UTC, validates and applies enrollment changes, with automatic reprocessing of affected claims for retroactive changes.

## Details

Primary enrollment source from benefits administration system (managed by HR/Benefits team). Process flow: EDI 834 file lands on SFTP at ~02:00 UTC nightly, batch job picks up, validates, and applies enrollment changes. If change is retroactive (effective date in past), triggers automatic reprocessing of affected claims. Processing typically completes by 04:00 UTC. File size variations indicate potential issues - 10x normal size might be bulk correction, unexpectedly small might indicate upstream system problems.
