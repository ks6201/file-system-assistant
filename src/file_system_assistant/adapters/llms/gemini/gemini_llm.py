
from logging import Logger
import os

from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from file_system_assistant.app.configs.constants import Constants
from file_system_assistant.app.services.container import Container
from file_system_assistant.core.ports.llm.llm import LLM
from file_system_assistant.core.ports.llm.llm_input import LLMInput
from file_system_assistant.core.ports.llm.llm_response import LLMResponse
from file_system_assistant.core.ports.tools_registry.tools_registry import ToolsRegistry
from file_system_assistant.core.types.result import Result

class GeminiLLM(LLM):

    def __init__(self, tools_registry: ToolsRegistry):
        super().__init__(tools_registry)

        self.client = genai.Client(
            api_key=os.getenv(Constants.GOOGLE_API_KEY_ENV)
        )

        self.config = types.GenerateContentConfig(
            tools = [tool.tool_fn for tool in self._tools_registry.tools()]
        )

        self.chat = self.client.chats.create(
            model="gemini-3-flash-preview",
            config=self.config
        )
        
        self.logger = Container.resolve(Logger)

    def generate(self, llm_input: LLMInput) -> Result[LLMResponse, str]:
        try:
            response = self.chat.send_message(message=llm_input.content) # type: ignore

            llm_resp = LLMResponse(
                response.text or "", 
                response.usage_metadata.prompt_token_count or 0,  # type: ignore
                response.usage_metadata.candidates_token_count or 0 # type: ignore
            )

            if not llm_resp.text:
                self.logger.warning("Empty response from GeminiLLM")

            return Result.ok(llm_resp)
        
        except ServerError as e:
            self.logger.error(e)
            return Result.err(
                "The AI service is temporarily unavailable."
                "Please try again in a few moments."
            )

        except ClientError as e:
            self.logger.error(e)

            if e.code == 429:
                return Result.err(
                    "You have reached your usage limit."
                    "Please wait before making additional requests."
                )
            else:
                return Result.err(
                    "Your request could not be processed."
                    "Please verify your input and try again."
                )

        except Exception as e:
            self.logger.error(e)
            return Result.err(
                "Something went wrong while processing your request."
            )
        
    def close(self):
        self.client.close()