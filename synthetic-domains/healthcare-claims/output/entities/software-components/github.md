---
type: software-component
id: github
name: GitHub
description: Source code repository and CI/CD platform hosting clearview-health organization
status: active
tags:
- infrastructure
- external
source_documents:
- deployment-guide.txt
confidence: 0.9
used_by:
- github-actions-cicd-pipeline
---

# GitHub

## Overview

GitHub serves as both the source code repository for all claims platform services and the CI/CD execution platform via GitHub Actions. All deployments originate from commits to this platform.

## Details

Houses the clearview-health organization with repositories for all claims platform services. GitHub Actions provides the CI/CD execution environment for the six-stage deployment pipeline. Access to the clearview-health org is a prerequisite for any deployment activities. The platform also hosts the 'rollback' workflow used for emergency rollbacks to previous image versions.
