import time
from mlx_lm import load
from . import ALL_AGENTS


MODEL_ID = "mlx-community/Meta-Llama-3.1-8B-Instruct-4bit"


class SFDRunner:
    def __init__(self):
        print(f"Caricamento modello: {MODEL_ID}")
        t0 = time.time()
        self._model, self._tokenizer = load(MODEL_ID)
        print(f"Modello caricato in {time.time() - t0:.1f}s")
        self._agents = [cls(self._model, self._tokenizer) for cls in ALL_AGENTS]

    def run(self, mi: str) -> dict:
        """Fase 1 — ogni AI risponde sequenzialmente al M.I."""
        results = {}
        print(f"\n{'='*60}")
        print(f"M.I.: {mi}")
        print(f"{'='*60}\n")
        for agent in self._agents:
            print(f"[{agent.NAME}] in elaborazione...")
            t0 = time.time()
            response = agent.respond(mi)
            elapsed = time.time() - t0
            results[agent.NAME] = response
            print(f"[{agent.NAME}] risposto in {elapsed:.1f}s\n")
        return results


def main():
    runner = SFDRunner()
    mi = "Come potremmo ridurre la povertà in Italia?"
    responses = runner.run(mi)

    print("\n" + "="*60)
    print("RISPOSTE COMPLETE")
    print("="*60)
    for name, response in responses.items():
        print(f"\n{'—'*40}")
        print(f"  {name.upper()}")
        print(f"{'—'*40}")
        print(response)

    return responses


if __name__ == "__main__":
    main()
