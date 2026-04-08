# 📄 Contract Negotiation Environment (OpenEnv Compatible)

This project implements a contract negotiation environment where intelligent agents make decisions such as accepting clauses, proposing edits, or escalating issues based on policy constraints.

The system is designed as a reinforcement-style environment with a reward-driven evaluation mechanism, enabling comparison between different agent strategies including rule-based and LLM-based approaches.

---

## 🚀 Features

- 🔧 FastAPI-based environment with REST API endpoints
- 📊 Reward-based evaluation system for decision quality
- 🤖 Multiple agents:
  - Rule-based agent (baseline)
  - LLM-based agent (local, via Ollama)
  - Hybrid agent (LLM + rule corrections)
- 🌐 Interactive frontend (HTML + JS)
- 📦 Dockerized and deployed on Hugging Face Spaces
- 📈 Evaluation system for comparing agent performance

---

## 🧠 Environment Design

### Actions
- `accept` → Accept clause if compliant
- `propose_edit` → Suggest modification
- `escalate` → Flag high-risk conflicts

### State Representation
```json
{
  "state": {
    "clause": "...",
    "policy": "...",
    "risk_level": "...",
    "vendor_importance": "..."
  }
}
