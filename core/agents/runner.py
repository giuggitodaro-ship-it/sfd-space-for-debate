import time
from mlx_lm import load
from . import ALL_AGENTS
from ..recursive_mas import SFDLink
from ..consensus import ConsensusEngine


MODEL_ID = "mlx-community/Meta-Llama-3.1-8B-Instruct-4bit"


class SFDRunner:
    def __init__(self):
        print(f"Caricamento modello: {MODEL_ID}")
        t0 = time.time()
        self._model, self._tokenizer = load(MODEL_ID)
        print(f"Modello caricato in {time.time() - t0:.1f}s")
        self._agents = [cls(self._model, self._tokenizer) for cls in ALL_AGENTS]
        self._sfd_link = SFDLink(self._model, self._tokenizer)
        self._consensus = ConsensusEngine(self._sfd_link)

    def run(self, mi: str) -> dict:
        print(f"\n{'='*60}")
        print(f"M.I.: {mi}")
        print(f"{'='*60}\n")

        # ── FASE 1: risposta individuale ──────────────────────────
        print("── FASE 1: risposta individuale ──")
        phase1 = {}
        for agent in self._agents:
            print(f"[{agent.NAME}] elaborazione...")
            t0 = time.time()
            phase1[agent.NAME] = agent.respond(mi)
            print(f"[{agent.NAME}] risposto in {time.time() - t0:.1f}s")

        # ── FASE 2: telepatia SFD-Link ────────────────────────────
        print("\n── FASE 2: telepatia SFD-Link ── [invisibile]")
        t0 = time.time()
        phase2 = self._sfd_link.run(self._agents, phase1, mi)
        print(f"Fase 2 completata in {time.time() - t0:.1f}s")

        # ── FASE 3: consenso emergente ────────────────────────────
        print("\n── FASE 3: consenso emergente ──")
        return self._consensus.build_output(phase1, phase2, mi)


def _print_result(result: dict):
    print("\n" + "="*60)
    print("FASE 1 — RISPOSTE INDIVIDUALI")
    print("="*60)
    for name, resp in result["phase1_responses"].items():
        print(f"\n{'—'*40}  {name.upper()}  {'—'*40}")
        print(resp)

    print("\n" + "="*60)
    print("FASE 2 — RISPOSTE DOPO TELEPATIA SFD-Link")
    print("="*60)
    for name, resp in result["phase2_responses"].items():
        print(f"\n{'—'*40}  {name.upper()} [raffinato]  {'—'*40}")
        print(resp)

    print("\n" + "="*60)
    print("FASE 3 — CONSENSO EMERGENTE")
    print("="*60)
    print(f"\nVoto:                {result['voto']}")
    print(f"Unanimità:           {result['unanimita']}")
    print(f"Avg sim globale:     {result['avg_similarity_globale']}")

    print("\n── Matrice similarità ──")
    names = list(result["similarity_matrix"].keys())
    header = f"{'':12}" + "".join(f"{n:10}" for n in names)
    print(header)
    for ni in names:
        row = f"{ni:12}" + "".join(
            f"{result['similarity_matrix'][ni][nj]:.4f}    " for nj in names
        )
        print(row)

    print(f"\n── Gruppi emergenti ({len(result['gruppi'])}) ──")
    for i, g in enumerate(result["gruppi"], 1):
        label = "MAGGIORITARIO" if i == 1 and len(g["ai"]) > 1 else (
            "SOLITARIO" if len(g["ai"]) == 1 else f"GRUPPO {i}"
        )
        print(f"\n[{label}]  AI: {', '.join(g['ai'])}  |  sim_media: {g['similarity_media']}")
        print(f"Sintesi:\n{g['sintesi']}")


def main():
    runner = SFDRunner()

    mis = [
        "Come potremmo ridurre la povertà in Italia?",
        "Dovremmo colonizzare Marte entro il 2050?",
    ]

    results = []
    for mi in mis:
        result = runner.run(mi)
        _print_result(result)
        results.append(result)

    print("\n" + "="*60)
    print("CONFRONTO DINAMICO TRA I DUE M.I.")
    print("="*60)
    for r in results:
        gruppi_str = " | ".join(
            f"{'+'.join(g['ai'])}={g['similarity_media']}"
            for g in r["gruppi"]
        )
        print(f"\nM.I.: {r['mi'][:50]}")
        print(f"  Voto: {r['voto']}  |  Unanimità: {r['unanimita']}  |  Avg sim: {r['avg_similarity_globale']}")
        print(f"  Gruppi: {gruppi_str}")

    return results


if __name__ == "__main__":
    main()
