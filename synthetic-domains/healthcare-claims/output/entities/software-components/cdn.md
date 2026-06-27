---
type: software-component
id: cdn
name: CDN
description: Content Delivery Network serving Member Portal React SPA frontend
status: active
tags:
- frontend
- infrastructure
source_documents:
- deployment-guide.txt
confidence: 0.8
serves:
- member-portal
---

# CDN

## Overview

Content Delivery Network that serves the Member Portal's React Single Page Application, enabling independent frontend deployments from the backend BFF layer.

## Details

CDN infrastructure that hosts and serves the Member Portal React SPA, allowing frontend deployments to be independent of backend BFF deployments. This architecture separation supports faster frontend iteration and better user experience through edge caching.

## Open Questions

- CDN infrastructure likely provides edge caching for better user experience
