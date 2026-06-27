---
type: domain-logic
id: provider-data-update-restrictions
name: Provider Data Update Restrictions
description: |-
  Business rules defining which provider data fields can be self-updated versus requiring manual review
status: active
tags:
- data-governance
- self-service-limits
- approval-required
source_documents:
- requirements-provider-portal-2023.txt
confidence: 0.95
enforced_by:
- provider-portal
applies_to:
- provider
---

# Provider Data Update Restrictions

## Overview

Business rules that govern which provider information can be self-updated through the portal versus requiring manual review for data integrity and compliance. These rules balance provider self-service convenience with data security and accuracy requirements.

## Details

Providers can self-update: address, phone, fax, email, office hours, accepting-new-patients flag, and practice locations (add, remove, edit). Providers CANNOT self-update: NPI, TIN, specialty, and credentials - these require manual review due to their critical nature for payment processing, network management, and credentialing compliance. Address and phone changes go through a 2-business-day approval queue handled by Provider Relations representatives to ensure accuracy.
