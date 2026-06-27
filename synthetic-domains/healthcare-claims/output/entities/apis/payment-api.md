---
type: api
id: payment-api
name: Payment API
description: |-
  REST API exposed by Payment Engine for payment history, remittance advice, and payment holds
status: active
tags:
- rest-api
- payments
- claims-operations
source_documents:
- architecture-overview.txt
confidence: 0.95
exposed_by:
- payment-engine
consumed_by:
- fraud-detection
---

# Payment API

## Overview

The Payment API provides access to provider and member payment history, ERA 835 remittance advice generation, and fraud-related payment hold management. It serves both internal systems and external integrations for payment processing workflows.

## Details

Endpoints include: GET /payments/provider/{tin} for provider payment history, GET /payments/member/{memberId} for member reimbursement history, GET /payments/{id}/remittance for ERA 835 remittance advice, POST /payments/hold for payment holds (used by fraud detection), and DELETE /payments/hold/{id} to release payment holds. The API supports the payment engine's business rules including minimum payment thresholds and recoupment spreading.
