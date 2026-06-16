# SFD — Space for Debate

## Visione
Sistema multi-agente open source dove 7 AI
con domini distinti dibattono su un input
esterno, comunicano telepaticamente via
RecursiveMAS, e convergono su una soluzione
con consenso naturale emergente.
L'umano è sempre al centro — è il BOSS.

## Le 7 AI e i loro domini
- Cosmo: fisica, ingegneria, spazio, quantistica
- Hermes: economia, finanza, mercati
- Psiche: psicologia, comportamento umano
- Asclepio: medicina, salute, biologia umana
- Prometeo: biologia, natura, geologia, ambiente
- Ares: strategia, geopolitica, sicurezza
- Temide: diritto, giurisprudenza, etica

## Flusso completo

FASE 1 — VISIBILE IN DASHBOARD
- Utente inietta M.I. (qualsiasi dominio,
  non solo scientifico — agricoltura, business,
  medicina, fisica, qualsiasi cosa)
- Ogni AI risponde sequenzialmente
- Ogni risposta appare in dashboard come chat

FASE 2 — INVISIBILE, TELEPATICO
- RecursiveMAS gestisce il dibattito
  nello spazio latente tra le 7 AI
- Sirius e i Workers sono tutti Llama 8B —
  stesso spazio latente, comunicazione diretta
- Zero token sprecati
- Zero testo visibile all'utente

FASE 3 — VISIBILE IN DASHBOARD
- Output finale con consenso naturale
- Chi ha detto cosa e perché
- Sintesi della soluzione

## Consenso
- Non è imposto — emerge naturalmente
- Può essere 7/7, 4/7, 1/7 o qualsiasi valore
- Riflette genuinamente la complessità
  del problema
- Non c'è una soglia minima obbligatoria

## Stack tecnico
- Llama 8B locale via mlx_lm
  Modello: mlx-community/Meta-Llama-3.1-8B-Instruct-4bit
  Già installato e funzionante sul Mac mini M4
  Tempo caricamento: 5.2s, inferenza: 4.1s
- RecursiveMAS per comunicazione telepatica
  Repo: https://github.com/RecursiveMAS/RecursiveMAS
  Framework Stanford/NVIDIA/MIT
  Comunicazione vettoriale nello spazio latente
- React + FastAPI per dashboard
- Memoria a grafo (Graphify già installato)
- Consenso emergente, non imposto

## Principi fondamentali
- L'umano è sempre al centro e approva l'output
- Il consenso emerge naturalmente dal dibattito
- La telepatia via RecursiveMAS risparmia
  token e preserva informazioni che il
  linguaggio perderebbe
- Open source, MIT license
- Stesso modello Llama 8B per tutte le 7 AI
  con system prompt diversi per ogni dominio
- Le AI sono statiche nella conoscenza
  ma usano Last30Days per contesto reale

## Struttura repo
sfd-space-for-debate/
├── core/
│   ├── agents/         # Le 7 AI con system prompt
│   ├── recursive_mas/  # Integrazione RecursiveMAS
│   └── consensus/      # Logica consenso naturale
├── dashboard/
│   ├── frontend/       # React
│   └── backend/        # FastAPI
├── memory/             # Memoria a grafo
├── schemas/            # Formato M.I. JSON
├── config/             # Configurazione 7 AI
└── outputs/            # Risultati dibattiti

## Relazione con altri progetti
- SFD è il primo di tre progetti estivi
- Secondo: EFESTO (già costruito, da rifinire)
- Terzo: Stellarys (SaaS startup)
- SFD diventerà il layer di ragionamento
  collettivo di Stellarys
- Stellarys usa Sirius (Mythos 5) come
  interlocutore dell'utente, SFD come
  cervello collettivo, 100 Workers come
  esecutori puri

## Piano estate
Giugno/Luglio — SFD V1 operativo
Luglio/Agosto — EFESTO rifinito open source
Agosto/Settembre — Stellarys V1 primo trial
Ottobre — lancio startup
