---
type: system
id: provider-portal
name: Provider Self-Service Portal
description: |-
  Self-service web portal for healthcare providers to manage their information and interact with Clearview
status: planned
tags:
- provider-facing
- self-service
- web-portal
- needs-review
source_documents:
- requirements-provider-portal-2023.txt
confidence: 0.9
owned_by:
- provider-network
communicates_with:
- provider-directory
- payment-engine
- pre-auth-service
---

# Provider Self-Service Portal

## Overview

A proposed provider-facing web portal that would allow healthcare providers to update demographic information, upload credentialing documents, view network participation status, and access payment history. The system was designed to reduce manual processing workload for the Provider Network team by enabling provider self-service.

## Details

The Provider Portal would serve as the primary interface for Clearview's 14K+ contracted providers to manage their relationship with the health plan. Core functionality includes profile management (address, phone, practice locations), credentialing document upload (medical license, DEA certificate, malpractice insurance), network status viewing, fee schedule access, and payment history with ERA 835 download capability. The system would implement role-based access control with FIDO2/WebAuthn authentication and integrate with Provider Directory, Payment Engine, and potentially Pre-Auth Service. The project was originally planned for 2024 delivery but was paused in December 2023 due to Rules Engine migration priority, with potential restart in Q1 2026.
