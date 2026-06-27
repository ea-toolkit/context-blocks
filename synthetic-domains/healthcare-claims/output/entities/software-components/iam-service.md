---
type: software-component
id: iam-service
name: IAM Service
description: |-
  Identity and Access Management service providing OAuth 2.0 token authentication for API access
status: active
tags:
- authentication
- oauth2
- infrastructure
source_documents:
- eligibility-api-reference.txt
confidence: 0.9
used_by:
- eligibility-api-v2
- claims-gateway
- rules-engine
---

# IAM Service

## Overview

Authentication service at https://auth.clearviewhealth.internal/oauth/token that issues Bearer tokens for API access. Supports client credentials grant type with configurable scopes for service-to-service authentication.

## Details

The IAM service implements OAuth 2.0 client credentials flow for API authentication, requiring client_id, client_secret, grant_type (client_credentials), and scope parameters. For Eligibility API access, clients request 'eligibility.read' scope to obtain Bearer tokens. The service appears to be Clearview's central authentication infrastructure serving multiple internal APIs, following standard OAuth 2.0 patterns for service-to-service authentication. Token management, expiration, and refresh policies are not documented but would be critical for production operations.
