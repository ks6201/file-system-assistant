
from logging import Logger


from file_system_assistant.adapters.llms.llm_factory import LLMFactory
from file_system_assistant.app.configs import register_tools
from file_system_assistant.app.configs.constants import Constants

from file_system_assistant.app.configs.logging.logging_config import FSALogger
from file_system_assistant.app.configs.singleton import register_singletons
from file_system_assistant.app.ports.console_in import ConsoleIn
from file_system_assistant.app.ports.console_out import ConsoleOut
from file_system_assistant.app.services import bootstrap
from file_system_assistant.app.services.container import Container
from file_system_assistant.app.utils import get_prompt_text, select_llm_provider
from file_system_assistant.core.ports.llm.llm_input import LLMRole
from file_system_assistant.app.services.file_system_assistant import FileSystemAssistant

@bootstrap([
    FSALogger.init,
    register_singletons,
    register_tools
])
def main():

    logger = Container.resolve(Logger)

    cout = Container.resolve(ConsoleOut)

    llm_provider = select_llm_provider()

    llm = LLMFactory.create(llm_provider)
    
    fsa = FileSystemAssistant(llm, cout)

    cin = Container.resolve(ConsoleIn)

    while True:
        try:
            user_query = cin.read_line(
                get_prompt_text(LLMRole.USER)
            )
            
            if not user_query.strip() or user_query.lower() in (Constants.QUIT, Constants.EXIT):
                break

            response = fsa.ask(user_query)
            
            cout.write_block(f"{get_prompt_text(LLMRole.ASSISTANT)}{response}")
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"LLM failure: {e}")
            cout.write_block("An internal error occurred.")