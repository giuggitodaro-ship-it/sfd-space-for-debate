import time
import mlx.core as mx
from mlx_lm import load
from . import ALL_AGENTS
from ..recursive_mas import SFDLink


MODEL_ID = "mlx-community/Meta-Llama-3.1-8B-Instruct-4bit"


class SFDRunner:
    def __init__(self):
        print(f"Caricamento modello: {MODEL_ID}")
        t0 = time.time()
        self._model, self._tokenizer = load(MODEL_ID)
        print(f"Modello caricato in {time.time() - t0:.1f}s")
        self._agents = [cls(self._model, self._tokenizer) for cls in ALL_AGENTS]
        self._sfd_link = SFDLink(self._model, self._tokenizer)

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
        consensus = self._compute_consensus(phase2)

        return {
            "risposte_fase1": phase1,
            "risposte_fase2": phase2,
            "consenso": consensus,
        }

    def _compute_consensus(self, phase2_responses: dict) -> dict:
        names = list(phase2_responses.keys())
        n = len(names)

        embeds = {
            name: self._sfd_link.extract_hidden(resp)
            for name, resp in phase2_responses.items()
        }

        def cosine_sim(a, b):
            return float(mx.sum(a * b) / (mx.sqrt(mx.sum(a * a)) * mx.sqrt(mx.sum(b * b))))

        sims = {
            (ni, nj): cosine_sim(embeds[ni], embeds[nj])
            for ni in names
            for nj in names
            if ni != nj
        }

        centrality = {
            name: sum(sims[(name, other)] for other in names if other != name) / (n - 1)
            for name in names
        }

        seed = max(centrality, key=centrality.get)
        threshold = 0.80

        convergenti = [
            name for name in names
            if name == seed or sims[(seed, name)] > threshold
        ]
        divergenti = [name for name in names if name not in convergenti]

        n_conv = len(convergenti)
        avg_sim = (
            sum(sims[(ni, nj)] for ni in convergenti for nj in convergenti if ni != nj)
            / (n_conv * (n_conv - 1))
            if n_conv > 1 else 1.0
        )

        return {
            "voto": f"{n_conv}/7",
            "convergenti": convergenti,
            "divergenti": divergenti,
            "avg_similarity": round(avg_sim, 4),
            "sintesi": phase2_responses[seed],
        }


def main():
    runner = SFDRunner()
    mi = "Come potremmo ridurre la povertà in Italia?"
    result = runner.run(mi)

    print("\n" + "="*60)
    print("FASE 1 — RISPOSTE INDIVIDUALI")
    print("="*60)
    for name, resp in result["risposte_fase1"].items():
        print(f"\n{'—'*40}")
        print(f"  {name.upper()}")
        print(f"{'—'*40}")
        print(resp)

    print("\n" + "="*60)
    print("FASE 2 — RISPOSTE DOPO TELEPATIA SFD-Link")
    print("="*60)
    for name, resp in result["risposte_fase2"].items():
        print(f"\n{'—'*40}")
        print(f"  {name.upper()} [raffinato]")
        print(f"{'—'*40}")
        print(resp)

    print("\n" + "="*60)
    print("FASE 3 — CONSENSO EMERGENTE")
    print("="*60)
    c = result["consenso"]
    print(f"\nVoto:         {c['voto']}")
    print(f"Convergenti:  {', '.join(c['convergenti'])}")
    print(f"Divergenti:   {', '.join(c['divergenti']) if c['divergenti'] else '—'}")
    print(f"Avg sim:      {c['avg_similarity']}")
    print(f"\nSINTESI (agente più centrale):")
    print(c["sintesi"])

    return result


if __name__ == "__main__":
    main()
