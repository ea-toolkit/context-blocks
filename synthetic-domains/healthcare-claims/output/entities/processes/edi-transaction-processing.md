---
type: process
id: edi-transaction-processing
name: EDI Transaction Processing
description: |-
  Standardized workflow for processing healthcare EDI transactions with clearinghouses and trading partners
status: active
tags:
- edi
- integration
- healthcare-standards
source_documents:
- integration-patterns-guide.txt
confidence: 0.95
executed_by:
- claims-gateway
uses:
- hashicorp-vault
---

# EDI Transaction Processing

## Overview

Standard workflow handling inbound and outbound EDI transactions including 837P/I claims, 270/271 eligibility, and 278 prior authorization. Processes both real-time and batch transactions through SFTP and AS2 protocols.

## Details

Five-step process: 1) Clearinghouse sends file via SFTP or real-time AS2, 2) Claims Gateway validates ISA/GS envelope segments, 3) Transaction sets parsed to internal data model, 4) Each transaction processed by type, 5) EDI 997/999 acknowledgment generated and returned. Supports multiple trading partners with partner-specific SFTP configurations stored in Vault. Strict validation of EDI field lengths (e.g., NPI exactly 10 digits, ICD-10 codes 3-7 characters).
