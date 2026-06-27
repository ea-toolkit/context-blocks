---
type: software-component
id: nodejs-bff
name: Node.js BFF
description: Backend For Frontend layer serving the Member Portal application
status: active
tags:
- infrastructure
- api-gateway
- member-facing
source_documents:
- claims-coding-standards.txt
confidence: 0.9
belongs_to:
- member-portal
---

# Node.js BFF

## Overview

Node.js-based Backend For Frontend (BFF) layer that sits between the Member Portal React application and backend microservices. Handles API aggregation, authentication, and member-specific data orchestration.

## Details

The Node.js BFF layer provides a dedicated backend service optimized for the Member Portal frontend needs. It handles API composition from multiple backend services, implements member-scoped security policies, and provides a simplified API surface for the React application. The BFF pattern allows the frontend team to evolve the member experience independently while maintaining proper separation from the core claims processing services.
