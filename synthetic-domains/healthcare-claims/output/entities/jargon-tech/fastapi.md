---
type: jargon-tech
id: fastapi
name: FastAPI
description: Python web framework used for serving Fraud Detection service APIs
status: active
tags:
- infrastructure
- python-framework
- ml-serving
source_documents:
- claims-coding-standards.txt
confidence: 1.0
used_by:
- fraud-detection
---

# FastAPI

## Overview

Modern Python web framework used specifically for the Fraud Detection service. Provides high-performance async API capabilities suitable for machine learning model serving and real-time fraud scoring operations.

## Details

FastAPI serves as the web framework for the Fraud Detection service, providing async/await support and automatic API documentation generation. The framework choice aligns with the Python-based machine learning stack including scikit-learn and XGBoost models. FastAPI's performance characteristics and built-in validation make it well-suited for real-time fraud scoring APIs that need to respond quickly during claims adjudication.
