import mlx.core as mx
from mlx_lm.sample_utils import make_sampler


class SFDLink:
    """Native MLX latent-space communication bridge for SFD agents."""

    def __init__(self, model, tokenizer):
        self._model = model
        self._tokenizer = tokenizer
        self.dim = 4096  # Llama 8B hidden dim

    def extract_hidden(self, text: str) -> mx.array:
        """Extract last-token hidden state from text. Returns (4096,) vector."""
        tokens = self._tokenizer.encode(text)
        tokens_mx = mx.array([tokens])
        hidden = self._model.model(tokens_mx)  # (1, seq_len, 4096)
        mx.eval(hidden)
        return hidden[0, -1, :]  # (4096,)

    def aggregate(self, vectors: list) -> mx.array:
        """Mean pool N vectors → consensus (4096,) vector."""
        stacked = mx.stack(vectors)  # (N, 4096)
        result = mx.mean(stacked, axis=0)
        mx.eval(result)
        return result  # (4096,)

    def inject_consensus(
        self, system_prompt: str, consensus_vector: mx.array, mi: str
    ) -> str:
        """
        Inject consensus_vector as a virtual prefix token before the prompt.
        The model "feels" the collective hidden state without reading it as text.
        Returns the generated response string.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": mi},
        ]
        if hasattr(self._tokenizer, "apply_chat_template"):
            prompt_text = self._tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        else:
            prompt_text = (
                f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
                f"{system_prompt}<|eot_id|>"
                f"<|start_header_id|>user<|end_header_id|>\n\n"
                f"{mi}<|eot_id|>"
                f"<|start_header_id|>assistant<|end_header_id|>\n\n"
            )

        tokens = self._tokenizer.encode(prompt_text)
        tokens_mx = mx.array([tokens])

        # Embed prompt tokens then prepend consensus as virtual token #0
        token_embeds = self._model.model.embed_tokens(tokens_mx)  # (1, seq_len, 4096)
        consensus_embed = consensus_vector.reshape(1, 1, self.dim)
        combined = mx.concatenate([consensus_embed, token_embeds], axis=1)  # (1, seq_len+1, 4096)
        mx.eval(combined)

        # Prefill with combined embeddings, cache KV state
        cache = self._model.make_cache()
        logits = self._model(None, cache=cache, input_embeddings=combined)
        mx.eval(logits)

        eos = self._tokenizer.eos_token_id
        generated = []

        next_id = self._sample(logits[0, -1, :])
        for _ in range(500):
            if next_id == eos:
                break
            generated.append(next_id)
            logits = self._model(mx.array([[next_id]]), cache=cache)
            mx.eval(logits)
            next_id = self._sample(logits[0, -1, :])

        return self._tokenizer.decode(generated)

    def run(self, agents: list, phase1_responses: dict, mi: str) -> dict:
        """
        Full SFD-Link telepathy pass:
        1. Extract hidden state from each Phase 1 response
        2. Aggregate → consensus vector
        3. Each agent regenerates conditioned on consensus
        Returns dict {agent_name: refined_response}
        """
        vectors = [self.extract_hidden(resp) for resp in phase1_responses.values()]
        consensus = self.aggregate(vectors)

        phase2 = {}
        for agent in agents:
            print(f"  [SFD-Link] {agent.NAME} ← consenso latente...")
            phase2[agent.NAME] = self.inject_consensus(agent.SYSTEM_PROMPT, consensus, mi)

        return phase2

    def _sample(self, logits_1d: mx.array, temp: float = 0.75) -> int:
        if temp == 0:
            return int(mx.argmax(logits_1d).item())
        token = mx.random.categorical(logits_1d * (1.0 / temp))
        mx.eval(token)
        return int(token.item())
