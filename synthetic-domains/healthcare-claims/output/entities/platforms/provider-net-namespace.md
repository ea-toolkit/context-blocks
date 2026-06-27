---
type: platform
id: provider-net-namespace
name: Provider-Net Namespace
description: Kubernetes namespace hosting provider network services
status: active
tags:
- kubernetes
- provider-network
source_documents:
- deployment-guide.txt
confidence: 0.9
hosts:
- provider-directory
---

# Provider-Net Namespace

## Overview

Kubernetes namespace containing services related to provider network management, specifically the Provider Directory service.

## Details

Kubernetes namespace focused on provider network functionality. Contains Provider Directory service which manages provider master data, demographics, credentials, network status, and fee schedules. This organization reflects the provider network service domain.
