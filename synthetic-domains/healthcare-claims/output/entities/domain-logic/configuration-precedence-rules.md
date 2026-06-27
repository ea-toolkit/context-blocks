---
type: domain-logic
id: configuration-precedence-rules
name: Configuration Precedence Rules
description: |-
  Hierarchical configuration override rules from environment variables to application defaults
status: active
tags:
- configuration-management
- security
- environment-specific
source_documents:
- claims-coding-standards.txt
confidence: 1.0
uses:
- hashicorp-vault
---

# Configuration Precedence Rules

## Overview

Standardized configuration precedence hierarchy ensuring consistent behavior across all services. Higher precedence sources override lower ones, with environment variables taking priority over secrets, ConfigMaps, and application defaults.

## Details

Configuration precedence follows this hierarchy from highest to lowest: 1) Environment variables, 2) Vault secrets, 3) ConfigMap values, 4) Application config defaults. This ensures environment-specific overrides work consistently while maintaining secure secret management and reasonable defaults. The rule prohibits putting environment-specific values directly in application config files, requiring use of ConfigMaps for environment-specific values and Vault for secrets.
