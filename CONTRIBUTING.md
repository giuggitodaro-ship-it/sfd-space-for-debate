# Contributing to SFD

## Come contribuire

### Bug report

Apri una issue con:
- Descrizione del problema
- Passi per riprodurlo
- Output dell'errore
- Versione macOS e chip Apple Silicon

### Nuova feature

1. Apri una issue prima di iniziare — discutiamo l'approccio
2. Fork del repo
3. Crea un branch: `git checkout -b feat/nome-feature`
4. Commit con messaggi chiari (`feat:`, `fix:`, `refactor:`)
5. Apri una PR verso `main`

---

## Aree prioritarie

### Nuove AI (8ª, 9ª...)

Ogni AI è un file in `core/agents/`. Per aggiungerne una:

```python
# core/agents/nome.py
from .base import Agent

class NomeAI(Agent):
    NAME = "NomeAI"
    SYSTEM_PROMPT = """Sei X, entità di ragionamento nel sistema SFD...
    
    MODO DI RAGIONARE: ...
    CARATTERE: ...
    FORMATO RISPOSTA: ...
    Rispondi sempre in italiano. Massimo 150 parole."""
```

Poi aggiungi in `core/agents/__init__.py`.

### Threshold dinamico

`ConsensusEngine.find_convergent_groups(threshold=0.85)` — il threshold è configurabile. Esplorare threshold adattivi basati sulla distribuzione reale delle similarità del debate.

### Streaming SSE

Il backend attualmente blocca fino al completamento (~5 min). Implementare SSE con `sse-starlette` per aggiornamenti in tempo reale su Fase 1 → Fase 2 → Fase 3.

### Memoria a grafo

`memory/` è predisposta. Integrare Graphify per memorizzare i debate precedenti e le connessioni tra M.I. simili.

### Porta su Linux/cloud

SFD usa MLX che è Apple Silicon only. Per Linux serve sostituire `mlx_lm` con `transformers` + CUDA/CPU. L'interfaccia di `SFDRunner` è identica — solo il backend di inferenza cambia.

---

## Principi del progetto

- **Nessun cloud** — tutto gira localmente
- **Consenso emergente** — non imposto, non hardcoded
- **L'umano approva** — SFD è un sistema di supporto, non di decisione autonoma
- **Stesso modello per tutte le AI** — la specializzazione viene dal system prompt, non da modelli diversi

---

## Setup sviluppo

```bash
git clone https://github.com/giuggitodaro-ship-it/sfd-space-for-debate
cd sfd-space-for-debate
pip install -r requirements.txt

# Test rapido senza dashboard
python3 -m core.agents.runner
```

Per testare una singola AI:

```python
from mlx_lm import load
from core.agents.ares import Ares

model, tokenizer = load("mlx-community/Meta-Llama-3.1-8B-Instruct-4bit")
ares = Ares(model, tokenizer)
print(ares.respond("Dovremmo entrare nella NATO?"))
```
