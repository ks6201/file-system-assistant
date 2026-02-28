


from logging import Logger
import sys

from file_system_assistant.app.ports.console_out import ConsoleOut
from file_system_assistant.app.services.container import Container
from file_system_assistant.core.ports.llm.llm import LLM
from file_system_assistant.core.ports.llm.llm_input import LLMInput, LLMRole
from file_system_assistant.app.configs.file_system_assistant_prompt import FILE_SYSTEM_ASSISTANT_PROMPT

class FileSystemAssistant:

    def __init__(
            self,
            llm: LLM,
            console: ConsoleOut
    ) -> None:
        self.logger = Container.resolve(Logger)
        
        self.__llm = llm
        self.__console = console
        
        self.logger.info(
            "Initializing File System Assistant...",
            extra={"console": True}
        )

        self.__llm.generate(
            LLMInput(
                role=LLMRole.ASSISTANT,
                content=FILE_SYSTEM_ASSISTANT_PROMPT
            )
        )
        

        self.__console.clear_screen()

        # self.__console.write_line("Hi! I'm your File System Assistant. How can I help you with your files today?\n")

    
    def ask(self, query: str) -> str:
        llm_input = LLMInput(
            role=LLMRole.USER,
            content=query
        )        
        result = self.__llm.generate(llm_input)

        if result.is_err():
            err = result.unwrap_err()

            self.__console.write_error_block(err)
            self.__console.write_line("Quitting...")
    
            self.close()
            sys.exit(1)

        llm_resp = result.unwrap()

        self.logger.info(f"Input token used {llm_resp.input_tokens}")
        self.logger.info(f"Output token used {llm_resp.output_tokens}")

        return llm_resp.text
    
    def close(self):
        self.__llm.close()