---
type: platform
id: member-svc-namespace
name: Member-Svc Namespace
description: Kubernetes namespace hosting member-facing services
status: active
tags:
- kubernetes
- member-services
source_documents:
- deployment-guide.txt
confidence: 0.9
hosts:
- eligibility-service
- nodejs-bff
---

# Member-Svc Namespace

## Overview

Kubernetes namespace containing services that directly serve members: Eligibility Service and Member Portal BFF layer.

## Details

Kubernetes namespace that groups member-focused services. Contains Eligibility Service (member enrollment and benefit verification) and Member Portal BFF (backend-for-frontend layer supporting the member portal). This organization reflects the member-centric service grouping.
