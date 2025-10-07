
---

## Table of Contents

* [Overview](#-overview)
* [Core Features](#-core-features)
* [System Architecture](#-system-architecture)
* [Directory Structure](#-directory-structure)
* [Setup & Installation](#-setup--installation)
* [Usage](#-usage)
* [Incremental Updates](#-incremental-updates)
* [Legend: Actions Explained](#-legend-actions-explained)
* [Goals & KPIs](#-goals--kpis)
* [Limitations & Future Enhancements](#-limitations--future-enhancements)

---

## Problem Statement:


In today's landscape, Large Language Models (LLMs) rely on diverse sources of information, such as the internet, presentations, databases, and more, to research topics. However, a significant challenge arises from the varying levels of credibility across these sources. Credibility is not only source-dependent but also context-specific, varying with the nature of the statement and the source providing it.
For instance, in an investor presentation, a CEO claiming to be a cybersecurity expert may be less credible due to potential bias, whereas statements about the company's challenges might carry more weight. Similarly, a commercial claiming a product is "the best toothpaste in the world" is inherently less credible than an independent, unbiased research study. Even in research, funding sources can introduce bias, further complicating credibility assessment.
The goal is to develop a system that evaluates and contextualizes the credibility of information, assigns it a credibility score, and takes real-time actions to enhance the factual accuracy of certain claims. By dynamically allocating effort based on the credibility score, the system ensures more reliable and trustworthy insights, validating claims, providing warnings, or even removing them, enabling LLMs to conduct deeper and more accurate research.

---

## Core Features

**Multi-format ingestion** — Supports `.pdf`, `.docx`, `.txt` and plain text
**Automatic claim extraction** — Detects atomic claims for granular scoring
**Source credibility weighting** — Uses source metadata and context signals
**Heuristic scoring model** — Calculates trust scores (0–100) based on metadata, corroboration, and declared conflicts
**Incremental updates** — Dynamically re-scores data when new evidence is added
**Explainable output** — Each claim is scored with suggested action (`validate`, `warn`, `remove`)

---

## 🏗️ System Architecture

```
             ┌──────────────────────────────────┐
             │          Document Loader         │
             │  - PDF/DOCX/TXT ingestion        │
             │  - Text extraction & cleaning    │
             └──────────────────────────────────┘
                            │
                            ▼
             ┌──────────────────────────────────┐
             │       Claim Extraction Engine    │
             │  - Sentence segmentation         │
             │  - Atomic claim identification   │
             └──────────────────────────────────┘
                            │
                            ▼
             ┌──────────────────────────────────┐
             │        Credibility Scorer        │
             │  - Source weighting              │
             │  - Conflict of interest checks   │
             │  - Corroboration via embeddings  │
             └──────────────────────────────────┘
                            │
                            ▼
             ┌──────────────────────────────────┐
             │    Incremental Update Pipeline   │
             │  - Real-time rescoring           │
             │  - Evidence refresh              │
             └──────────────────────────────────┘
```

---

## Directory Structure

```
Wand_Synthesis_Test_Task/
│
├─ 📂 Data/
│   ├─ Investor_Pitch.pdf
│   ├─ Research_Study.docx
│   └─ market_report.txt
│
├─ 📂 Documents/
│   ├─ Goals_and_KPI's.pdf
│   ├─ Agent_Design.pdf
│   ├─ Infrastructure_Sketch.pdf
│   ├─ Limitations_and_Future_Enhancements.pdf
│   └─ Solution_Architecture_High_Level_Flow.pdf
│
├─ main.py
├─ main_engine.py
├─ credibility_updater.py
├─ document_loader.py
├─ embeddings.py
├─ scoring.py
├─ utils.py
├─ config.py
├─ requirements.txt
└─ README.md
```

---

## ⚙️ Setup & Installation

```bash
git clone https://github.com/bit-w1zard/Wand_Synthesis_Test_TasK.git
cd Wand_Synthesis_Test_Task

# (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

Run the main engine:

```bash
python main.py
```

Example workflow (`main.py`):

```python
from main_engine import CredibilityEngine

eng = CredibilityEngine()
eng.ingest_file("sourceC", "Data/Investor_Pitch.pdf", {
    "type": "investor_presentation",
    "domain": "company.com",
    "declared_conflict": True
})

eng.rescore_incremental()
print(eng.report())
```

Output example:

```json
[
  {
    "text": "Our CEO, Jane Smith, is a world-renowned cybersecurity expert.",
    "source": "sourceC",
    "score": 45.0,
    "action": "remove"
  },
  {
    "text": "Independent auditors reported revenue growth was 60% in FY2024.",
    "source": "sourceC",
    "score": 99.0,
    "action": "validate"
  }
]
```

---

## Incremental Updates

Add new evidence and automatically refresh all scores:

```python
eng.incremental_update(
    "sourceC",
    "Independent auditors reported revenue growth was 60% in FY2024.",
    {"type": "licensed_database", "domain": "pitchbook.com"}
)
```

---

## Legend: Actions Explained

Each claim is assigned one of the following actions based on its credibility score and metadata:

| Action         | Meaning                                                                                                         | Typical Score Range | Recommended Next Step                                     |
| -------------- | --------------------------------------------------------------------------------------------------------------- | ------------------- | --------------------------------------------------------- |
| ✅ **VALIDATE** | The claim is supported by strong evidence, reliable sources, and no conflicts of interest.                      | `> 80`              | Can be confidently used or published.                     |
| ⚠️ **WARN**    | The claim has partial evidence or moderate credibility but may require additional review or cross-verification. | `50 – 80`           | Investigate further before relying on it.                 |
| ❌ **REMOVE**   | The claim is low-credibility, biased, unverifiable, or from an unreliable source.                               | `< 50`              | Should be excluded from official reports or model inputs. |

---

## Goals & KPIs

(See `Documents/Goals_and_KPI's.pdf` for details.)

---

## Limitations & Future Enhancements
# Limitations:
●​ The credibility scoring relies on heuristic and metadata-based signals but does not
deeply understand the semantic content of the claims that is crucial.
●​ It cannot detect contextually misleading claims if they are phrased confidently.
●​ The claim text is parsed with Regex which is pattern dependent.
●​ The system does not cross-verify claims with external, authoritative knowledge sources,
does not cross-verify claims with external, authoritative knowledge sources.
●​ As a result, scores may inflate even if the claim is factually false but appears in a
high-reputation source.

# Future Enhancements:
●​ Integrate transformer-based models for deep semantic credibility scoring.
●​ Utilise spaCy, NER or LLM’s for context extraction and more accurate claim text parsing.
●​ Flag misinformation, logical fallacies, and unsupported correlations beyond keywords
and metadata via LLM’s.
●​ Add automated fact-checking pipelines using APIs.
●​ Cross-reference numerical claims and named entities in real-time.

(See `Documents/Limitations_and_Future_Enhancements.pdf` for more.)

---
