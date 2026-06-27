---
type: system
id: benefits-administration-system
name: Benefits Administration System
description: External HR/Benefits system that provides primary enrollment data to
  Clearview
status: active
tags:
- external
- enrollment
- hr-benefits
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.9
provides_data_to:
- eligibility-service
exposes:
- enrollment-api
produces:
- edi-834
owned_by:
- benefits-administration-team
---

# Benefits Administration System

## Overview

Primary source of enrollment data managed by HR/Benefits team (not engineering). Provides enrollment updates through real-time API, nightly EDI 834 files, and open enrollment batch loads.

## Details

External system owned by HR/Benefits team that serves as the authoritative source for member enrollment information. Provides three types of enrollment feeds: real-time API for individual enrollment changes, nightly batch EDI 834 files for group enrollment updates delivered via SFTP at ~02:00 UTC, and large batch loads during open enrollment periods (November-December). System is outside engineering control but critical dependency for Eligibility Service operations.
