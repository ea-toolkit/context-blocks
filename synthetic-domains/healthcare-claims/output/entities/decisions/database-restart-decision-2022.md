---
type: decision
id: database-restart-decision-2022
name: Database Restart Decision (2022 Outage)
description: |-
  Dana Okafor's decision to restart the Cloud SQL instance to resolve the table lock
status: active
tags:
- legacy-era
- incident-response
- high-risk
source_documents:
- postmortem-2022-eligibility-outage.txt
confidence: 1.0
made_by:
- dana-okafor
applies_to:
- cloud-sql-postgresql
resolved:
- september-2022-eligibility-outage
---

# Database Restart Decision (2022 Outage)

## Overview

During the September 2022 Eligibility Service outage, Dana Okafor made the decision to restart the entire Cloud SQL database instance after attempts to terminate the blocking migration query failed to fully release the table lock. This was a high-risk decision during a SEV-1 incident that ultimately resolved the issue.

## Details

At 09:35, Dana attempted to kill the migration query directly using pg_terminate_backend(), but the table lock wasn't fully released due to dependent transactions waiting. After 7 minutes of unsuccessful attempts to resolve the lock, Dana decided at 09:42 to restart the database instance. This was a significant decision during a SEV-1 incident because database restarts carry risk and extend downtime, but it was the only viable option to clear the persistent table lock. The restart took 13 minutes (09:42-09:55) and successfully resolved the issue.
