---
type: software-component
id: poetry
name: Poetry
description: Python dependency management tool used for Fraud Detection service
status: active
tags:
- infrastructure
- dependency-management
- python-ecosystem
source_documents:
- claims-coding-standards.txt
confidence: 1.0
used_by:
- fraud-detection
---

# Poetry

## Overview

Modern Python dependency management and packaging tool. Used specifically for the Fraud Detection service to handle Python package dependencies, virtual environments, and build processes.

## Details

Poetry manages Python dependencies for the Fraud Detection service, providing deterministic builds through lock files and virtual environment management. Handles the complex dependency graph of machine learning libraries including scikit-learn and XGBoost, ensuring reproducible builds across development and production environments. Poetry's dependency resolver helps avoid conflicts common in ML environments with competing package requirements.
