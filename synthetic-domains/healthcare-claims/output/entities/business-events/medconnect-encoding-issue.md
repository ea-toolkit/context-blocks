---
type: business-event
id: medconnect-encoding-issue
name: MedConnect Encoding Issue
description: |-
  SEV-2 incident when MedConnect Exchange changed character sets in EDI 837I batches without notification
status: active
tags:
- sev-2
- external-party
- edi-processing
source_documents:
- meeting-notes-quarterly-ops-review-2025q3.txt
confidence: 0.85
caused_by:
- medconnect-exchange
affects:
- claims-gateway
---

# MedConnect Encoding Issue

## Overview

SEV-2 incident during Q3 2025 when MedConnect Exchange changed character encoding in institutional claim batches without notifying Clearview, causing processing failures.

## Details

Severity-2 incident during Q3 2025 when MedConnect Exchange, one of Clearview's EDI clearinghouse partners, switched character sets in their EDI 837 Institutional claim batches without providing advance notification to Clearview. This caused processing failures in the claims intake pipeline until the encoding issue was identified and resolved. The incident highlights the dependency on external clearinghouse partners and the need for better change communication protocols.
