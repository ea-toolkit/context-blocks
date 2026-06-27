---
type: data-model
id: edi-837-institutional
name: EDI 837 Institutional
description: |-
  Electronic data interchange format for institutional healthcare claims (UB-04 equivalent)
status: active
tags:
- edi
- institutional-claims
- batch-processing
source_documents:
- architecture-overview.txt
confidence: 0.95
used_by:
- claims-gateway
contracts:
- claims-submission-api
---

# EDI 837 Institutional

## Overview

EDI 837 Institutional is the standard electronic format for submitting institutional healthcare claims such as hospital stays and facility services. It's the electronic equivalent of the UB-04 paper form and is processed in batch mode with 4-hour windows.

## Details

Standard EDI transaction format used for institutional healthcare services like hospital inpatient stays, emergency room visits, and other facility-based care. Contains detailed service information, room and board charges, pharmacy charges, and other institutional billing elements. Processed in batch mode with 4-hour processing windows due to the typically larger size and complexity of these claims compared to professional claims. The Claims Gateway handles format validation and routing to adjudication systems.
