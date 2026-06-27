---
type: process
id: institutional-claims-intake-batch
name: Institutional Claims Intake Batch
description: |-
  Scheduled batch job processing EDI 837I institutional claims files from clearinghouses
status: active
tags:
- batch-processing
- edi
- scheduled
source_documents:
- integration-patterns-guide.txt
confidence: 0.95
executed_by:
- claims-gateway
processes:
- edi-837-institutional
---

# Institutional Claims Intake Batch

## Overview

Automated batch job running every 4 hours to process institutional claims (EDI 837I) from clearinghouse SFTP drops. Validates, parses, and routes claims to adjudication with a 2,000 claim per batch limit.

## Details

Runs at 00:00, 04:00, 08:00, 12:00, 16:00, 20:00 UTC using Spring Batch framework. Claims Gateway picks up 837I files from clearinghouse SFTP, validates format, parses to internal model, inserts into claims table, and routes to adjudication. 2,000 claim batch size limit added after the 2024 connection pool incident to prevent resource exhaustion.
