from mlx_lm import generate
from mlx_lm.sample_utils import make_sampler


class Agent:
    NAME: str = ""
    SYSTEM_PROMPT: str = ""

    def __init__(self, model, tokenizer):
        self._model = model
        self._tokenizer = tokenizer

    def respond(self, mi: str) -> str:
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": mi},
        ]
        if hasattr(self._tokenizer, "apply_chat_template"):
            prompt = self._tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        else:
            prompt = (
                f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
                f"{self.SYSTEM_PROMPT}<|eot_id|>"
                f"<|start_header_id|>user<|end_header_id|>\n\n"
                f"{mi}<|eot_id|>"
                f"<|start_header_id|>assistant<|end_header_id|>\n\n"
            )
        return generate(
            self._model,
            self._tokenizer,
            prompt=prompt,
            max_tokens=500,
            sampler=make_sampler(temp=0.75),
            verbose=False,
        )
