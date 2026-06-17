# SFD — Space for Debate

**7 AI specializzate dibattono su qualsiasi domanda e convergono su un consenso emergente — tutto in locale, senza cloud.**

---

## Come funziona

```
INPUT (M.I.)
    │
    ▼
FASE 1 — Visibile
Ogni AI risponde dal suo dominio (fisica, economia, psicologia, medicina, ecologia, strategia, diritto)

    │
    ▼
FASE 2 — Invisibile (SFD-Link)
Le 7 AI comunicano telepaticamente nello spazio latente di Llama 8B.
Ogni AI riceve il vettore di consenso e raffina la sua risposta.

    │
    ▼
FASE 3 — Consenso emergente
Matrice di similarità 7×7 → componenti connesse → voto X/7.
Il consenso non è imposto — emerge dai dati.
```

---

## Stack tecnico

| Layer | Tech |
|-------|------|
| Modello LLM | `mlx-community/Meta-Llama-3.1-8B-Instruct-4bit` |
| Inferenza locale | [mlx-lm](https://github.com/ml-explore/mlx-lm) (Apple Silicon) |
| Comunicazione latente | SFD-Link — iniezione `input_embeddings` nativa MLX |
| Backend API | FastAPI + Uvicorn |
| Frontend | React 18 + Vite, CSS puro |

**Requisiti hardware:** Mac con chip Apple Silicon (M1/M2/M3/M4). ~8GB RAM unificata libera.

---

## Installazione

```bash
git clone https://github.com/giuggitodaro-ship-it/sfd-space-for-debate
cd sfd-space-for-debate
pip install -r requirements.txt
cd dashboard/frontend && npm install && cd ../..
```

Il modello (`Meta-Llama-3.1-8B-Instruct-4bit`, ~4.5GB) viene scaricato automaticamente al primo avvio da Hugging Face.

---

## Avvio

**Terminale 1 — Backend:**
```bash
uvicorn dashboard.backend.main:app --port 8000
```

**Terminale 2 — Frontend:**
```bash
cd dashboard/frontend && npm start
```

Apri `http://localhost:3000`.

> **Tempo di elaborazione:** ~5 minuti per debate completo (7 AI × Fase1 + SFD-Link Fase2 + consenso).

---

## Esempio di output

**M.I.:** *"Come potremmo ridurre la povertà in Italia?"*

```
Voto:            5/7
Convergenti:     Hermes, Psiche, Asclepio, Prometeo, Temide
Divergenti:      Cosmo, Ares
Avg similarity:  0.8916

Sintesi (agente più centrale — Prometeo):
La povertà in Italia richiede un approccio olistico che integri
formazione professionale, accesso ai servizi essenziali e
pianificazione urbana sostenibile...
```

**M.I.:** *"Dovremmo colonizzare Marte entro il 2050?"*

```
Voto:            3/7
Convergenti:     Hermes, Asclepio, Prometeo
Divergenti:      Cosmo, Psiche, Ares, Temide
Avg similarity:  0.5834
```

Stesso sistema, topic diverso → consenso diverso. Nessun valore hardcoded.

---

## Le 7 AI

| AI | Dominio | Carattere |
|----|---------|-----------|
| **Cosmo** | Fisica & Spazio | Traduce ogni problema in sistema fisico con variabili e metriche |
| **Hermes** | Economia | Legge ogni situazione come struttura di incentivi |
| **Psiche** | Psicologia | Identifica le dinamiche emotive e le resistenze umane |
| **Asclepio** | Medicina | Ragiona su dati clinici, popolazioni vulnerabili |
| **Prometeo** | Natura & Ecologia | Connessioni ecosistemiche, scale temporali lunghe |
| **Ares** | Strategia | Mappa giocatori, vulnerabilità, chi può sabotare |
| **Temide** | Diritto | Quadro normativo, diritti in conflitto, rischi legali |

---

## Struttura del progetto

```
sfd-space-for-debate/
├── core/
│   ├── agents/          # Le 7 AI con system prompt
│   │   ├── base.py      # Classe base Agent
│   │   ├── runner.py    # Orchestratore 3 fasi
│   │   └── *.py         # Un file per AI
│   ├── recursive_mas/
│   │   └── sfd_link.py  # Comunicazione latente SFD-Link
│   └── consensus/
│       └── engine.py    # ConsensusEngine — matrice similarità
├── dashboard/
│   ├── backend/
│   │   └── main.py      # FastAPI
│   └── frontend/
│       └── src/App.jsx  # React UI
└── requirements.txt
```

---

## Usarlo da CLI (senza dashboard)

```python
from core.agents.runner import SFDRunner

runner = SFDRunner()
result = runner.run("La tua domanda qui")

print(result["voto"])          # es. "5/7"
print(result["gruppi"])        # gruppi emergenti con sintesi
print(result["unanimita"])     # True/False
```

---

## Contribuire

Vedi [CONTRIBUTING.md](CONTRIBUTING.md).

---

MIT License — parte del progetto [Stellarys](https://github.com/giuggitodaro-ship-it).
