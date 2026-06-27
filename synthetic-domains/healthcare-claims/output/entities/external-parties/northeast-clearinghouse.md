---
type: external-party
id: northeast-clearinghouse
name: Northeast Clearinghouse
description: |-
  Primary healthcare clearinghouse handling ~60% of Clearview's EDI transaction volume
status: active
tags:
- trading-partner
- edi
- healthcare
source_documents:
- integration-patterns-guide.txt
confidence: 0.9
integrated_via:
- claims-gateway
---

# Northeast Clearinghouse

## Overview

Primary trading partner for EDI transactions, processing approximately 60% of Clearview's healthcare transaction volume. Integrated via SFTP and AS2 protocols with partner-specific directory structures.

## Details

Largest clearinghouse partner with dedicated SFTP configuration and credentials managed in Vault. Handles majority of inbound EDI 837P/I claims and outbound EDI 835 remittance advice. Uses standard healthcare EDI protocols with partner-specific directory structures for file exchange.
