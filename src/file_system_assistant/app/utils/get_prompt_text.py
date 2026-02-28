

from file_system_assistant.core.ports.llm.llm_input import LLMRole


def get_prompt_text(role: LLMRole):
    return f"[{role.capitalize()}]: "
