---
type: external-party
id: directsubmit
name: DirectSubmit
description: |-
  Healthcare clearinghouse handling ~15% of Clearview's EDI volume, mostly smaller provider groups
status: active
tags:
- trading-partner
- edi
- healthcare
- small-providers
source_documents:
- integration-patterns-guide.txt
confidence: 0.9
integrated_via:
- claims-gateway
---

# DirectSubmit

## Overview

Smaller trading partner for EDI transactions, processing approximately 15% of Clearview's healthcare transaction volume, primarily serving smaller provider groups. Integrated via SFTP and AS2 protocols.

## Details

Smallest of the three main clearinghouse partners, specializing in smaller provider groups that need EDI transaction services. Uses same SFTP/AS2 protocols as other partners with partner-specific configurations stored in Vault.
