---
type: software-component
id: trivy
name: Trivy
description: Container image vulnerability scanner used in CI/CD pipeline
status: active
tags:
- security
- external
source_documents:
- deployment-guide.txt
confidence: 0.85
used_by:
- github-actions-cicd-pipeline
---

# Trivy

## Overview

Container image security scanning tool integrated into the CI/CD pipeline's security scan stage to identify vulnerabilities in Docker images.

## Details

Security scanning tool that analyzes Docker container images for vulnerabilities during the CI/CD pipeline's security scan stage. Complements Snyk's dependency scanning by focusing specifically on container image security.
