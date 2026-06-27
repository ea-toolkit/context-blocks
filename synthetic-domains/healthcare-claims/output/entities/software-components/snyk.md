---
type: software-component
id: snyk
name: Snyk
description: Dependency vulnerability scanning tool used in CI/CD pipeline
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

# Snyk

## Overview

Security scanning tool integrated into the CI/CD pipeline's security scan stage to identify vulnerabilities in service dependencies.

## Details

Third-party security tool that scans service dependencies for known vulnerabilities during the CI/CD pipeline's security scan stage. Works alongside Trivy to provide comprehensive security scanning before images are built and deployed.
