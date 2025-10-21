# Architecture Overview

## Components
- **Python (ETL / ML)** — parses logs → normalizes events → applies rules + classifier → writes results to SQL  
- **.NET WebAPI** — endpoints `/analyze` and `/runs/{id}` → calls Python service  
- **Angular UI** — upload log → view categories + suggested fixes  
- **SQL DB** — dev = SQLite, prod = Azure SQL  
- **Docker/K8s** — containers for API & UI; K8s manifests for AKS deployment  

## Flow
1. UI uploads a log.  
2. WebAPI forwards to Python analyzer.  
3. Analyzer returns structured events + predicted classes.  
4. WebAPI stores in SQL and returns summary to UI.  
