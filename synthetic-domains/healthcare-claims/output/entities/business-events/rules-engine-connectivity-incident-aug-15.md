---
type: business-event
id: rules-engine-connectivity-incident-aug-15
name: Rules Engine Connectivity Incident (August 15)
description: |-
  SEV-1 incident caused by VPN tunnel failure to HealthLogic data center affecting claims processing
status: active
tags:
- sev-1
- external-dependency
- august-2025
source_documents:
- meeting-notes-quarterly-ops-review-2025q3.txt
confidence: 0.9
affects:
- rules-engine
caused_by:
- healthlogic-systems
---

# Rules Engine Connectivity Incident (August 15)

## Overview

45-minute SEV-1 incident on August 15, 2025 when VPN tunnel to HealthLogic's data center failed, disrupting rules engine connectivity and claims processing. External issue that reinforces need to migrate away from HealthLogic.

## Details

Severity-1 incident lasting 45 minutes on August 15, 2025 when the VPN tunnel between Clearview and HealthLogic's data center experienced a flap, causing connectivity issues with the Rules Engine. While the root cause was external to Clearview (HealthLogic's infrastructure issue), it disrupted claims processing and highlighted the dependency risk of using an external vendor system. This incident provides additional justification for the ongoing migration away from HealthLogic to an internal rules engine solution.
