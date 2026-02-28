from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    input_tokens: int
    output_tokens: int