# Automated Pre-Deployment Error Analyzer

Deployments often fail in tools such as **Ansible Tower** and **XL Release**.  
Engineers spend 15–30 minutes reading logs to find root causes.  

**This tool** automatically analyzes deployment logs, detects failure patterns, and suggests fixes — saving time and making issue triage consistent.

---

## 🎯 Goals (MVP)
- Ingest log files (Ansible Tower / XL Release)
- Normalize to a unified JSON schema
- Detect failure patterns via rules + ML
- Expose a .NET WebAPI endpoint
- Angular UI: upload log → see categorized issues
- Store runs and metrics in SQL (SQLite → Azure SQL later)
- Containerized with Docker → deployable on AKS later

---

## 🧩 Failure Taxonomy (v1)
| Category | Example |
|-----------|----------|
| Authentication | Invalid credentials |
| Network | DNS / TLS failure |
| Configuration | Missing variable |
| Dependency | Module not found |
| Syntax | Script error |
| Environment | Path issues |
| Resource Limits | Disk full, memory exhausted |
| Permissions | Access denied |
| Secrets | KeyVault access failure |
| Version | Package incompatibility |
| Timeout | Retry exhausted |
| External Service | API unavailable |

---

## 📈 Success Metrics
| Metric | Target |
|--------|--------|
| Macro-F1 | ≥ 0.80 |
| Coverage | ≥ 90 % |
| Speed | ≤ 2 s for 5 MB log |
| DX Improvement | ≥ 50 % faster diagnosis |

---

## 📂 Structure
api/ # .NET WebAPI
src-python/ # Parsing + Analysis
connectors/angular-ui/ # Front-end
docs/ # Docs & Specs
data/ # Sample logs
infra/ # Docker + K8s files
models/ # Saved ML models
notebooks/ # Experiments
scripts/ # Utilities
.github/workflows/ # CI/CD pipelines


---

### 🛠 Tech Stack
| Layer | Tools |
|-------|-------|
| Backend | .NET WebAPI |
| ML & Parsing | Python |
| Frontend | Angular |
| Database | SQL / SQLite |
| Deployment | Docker, K8s |
| Cloud | Azure |
| Dev Tools | Git, Copilot, Agile |

---

### 📜 License
MIT License