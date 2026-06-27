---
type: external-party
id: medconnect-exchange
name: MedConnect Exchange
description: Healthcare clearinghouse handling ~25% of Clearview's EDI transaction
  volume
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

# MedConnect Exchange

## Overview

Secondary trading partner for EDI transactions, processing approximately 25% of Clearview's healthcare transaction volume. Integrated via SFTP and AS2 protocols.

## Details

Mid-size clearinghouse partner with dedicated SFTP configuration and credentials managed in Vault. Handles quarter of inbound EDI transaction volume with same protocols as other trading partners but partner-specific directory structures.
