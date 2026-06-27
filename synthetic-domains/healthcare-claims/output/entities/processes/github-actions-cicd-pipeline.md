---
type: process
id: github-actions-cicd-pipeline
name: GitHub Actions CI/CD Pipeline
description: |-
  Six-stage continuous integration and deployment pipeline for all claims platform services
status: active
tags:
- infrastructure
- deployment
source_documents:
- deployment-guide.txt
confidence: 0.95
uses:
- github
integrates_with:
- artifact-registry
- snyk
- trivy
governed_by:
- payment-cycle-timing-constraints
---

# GitHub Actions CI/CD Pipeline

## Overview

The standardized CI/CD pipeline that all claims platform services use, built on GitHub Actions. It handles everything from code compilation through production deployment with manual approval gates and rollback capabilities.

## Details

Six-stage pipeline: 1) Build (compile, unit tests), 2) Test (integration tests against test containers), 3) Security scan (Snyk for dependencies, Trivy for container images), 4) Build image (Docker build, push to Artifact Registry), 5) Deploy to staging (automatic on merge to main), 6) Deploy to production (manual approval required). Production deployment requires all CI checks green, manual approval from Marcus Reeves, Priya Anand, or service tech lead, no active SEV-1 incidents, and avoidance of payment cycle windows (02:00-06:00 UTC) unless emergency. Supports both rolling update (default, zero downtime) and canary deployment strategies (10% traffic for 30 minutes then full rollout for high-risk changes). Rollback achieved by reverting merge commit or using GitHub Actions 'rollback' workflow to redeploy last known good image tag.
