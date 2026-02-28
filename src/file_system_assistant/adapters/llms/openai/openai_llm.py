


from dataclasses import asdict
import json
from logging import Logger
import os
from typing import Any

from openai.types.responses import Response, ResponseFunctionToolCall
from openai import APIError, AuthenticationError, BadRequestError, OpenAI, RateLimitError

from file_system_assistant.app.configs.constants import Constants
from file_system_assistant.app.services.container import Container
from file_system_assistant.core.ports.llm.llm import LLM
from file_system_assistant.core.ports.llm.llm_input import LLMInput, LLMRole
from file_system_assistant.core.ports.llm.llm_response import LLMResponse
from file_system_assistant.core.ports.tools_registry.tools_registry import ToolsRegistry
from file_system_assistant.core.types.result import Result


from openai import OpenAI
from openai import APIError, AuthenticationError, RateLimitError, BadRequestError
from dataclasses import asdict


class OpenAILLM(LLM):

    def __init__(self, tools_registry: ToolsRegistry) -> None:
        super().__init__(tools_registry)
        
        self.__client = OpenAI(
            api_key=os.getenv(Constants.OPENAI_API_KEY_ENV)
        )

        self.__tools = [ tool.tool_schema for tool in tools_registry.tools() ]

        self.__conversations: Any = []
        self.__model = "gpt-5-mini"
        
        self.logger = Container.resolve(Logger)

    def __generate(self, message: dict[str, Any]) -> Result[Response, str]:
        try:
            self.__conversations.append(message)

            response = self.__client.responses.create(
                model=self.__model,
                input=self.__conversations,
                tools=self.__tools, # type: ignore
            )

            return Result.ok(response)

        except AuthenticationError as e:
            self.logger.error(e)
            return Result.err(
                "Invalid API credentials."
            )

        except RateLimitError as e:
            self.logger.error(e)
            return Result.err(
                "Rate limit exceeded. Try again later."
            )

        except BadRequestError as e:
            self.logger.error(e)
            return Result.err(
                "Invalid request payload."
            )

        except APIError as e:
            self.logger.error(e)
            return Result.err(
                "AI service error."
            )

        except Exception as e:
            self.logger.error(e)
            return Result.err(
                "Unexpected error occurred."
            )

    def handle_tool_calls(
        self,
        response: Response,
        tool_calls: list[ResponseFunctionToolCall],
    ) -> Result[Response, str]:

        tool_call_results: list[Any] = []

        for tool_call in tool_calls:
            self.logger.info(f"Calling '{tool_call.name}' with Args: '{tool_call.arguments}'")

            tool = self._tools_registry.get_tool(tool_call.name)

            if tool is None:
                return Result.err(
                    f"Tool call failed: '{tool_call.name}'"
                )

            try:
            
                args = json.loads(tool_call.arguments)
                tool_call_result = tool.tool_fn(**args)
            
            except Exception as e:
                return Result.err(
                    f"Tool call failed: {tool_call.name} — {str(e)}"
                )

            tool_call_results.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(tool_call_result),
            })

        new_response = self.__client.responses.create(
            model=self.__model,
            previous_response_id=response.id,
            input=tool_call_results,
            tools=self.__tools, # type: ignore
        )

        return Result.ok(new_response)

    def generate(self, llm_input: LLMInput) -> Result[LLMResponse, str]:
        message = asdict(llm_input)

        result = self.__generate(message)

        if result.is_err():
            return Result.err(result.unwrap_err())
        
        response = result.unwrap()

        tool_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]
        
        while len(tool_calls) > 0:
            self.__conversations.append(
                asdict(
                    LLMInput(
                        role=LLMRole.ASSISTANT,
                        content=response.output_text
                    )
                )
            )

            call_result = self.handle_tool_calls(response, tool_calls)

            if call_result.is_err():
                return Result.err(call_result.unwrap_err())
            
            response = call_result.unwrap()

            tool_calls = [
                item for item in response.output
                if item.type == "function_call"
            ]

        output_text = response.output_text or "Something went wrong, please try again with same query."

        reply = asdict(LLMInput(
            role=LLMRole.ASSISTANT,
            content=output_text
        ))

        if output_text:
            self.__conversations.append(reply)
        else:
            self.logger.warning("Empty response from OpenAILLM")

        usage = response.usage

        llm_resp = LLMResponse(
            text=output_text,
            input_tokens=usage.input_tokens if usage else 0,
            output_tokens=usage.output_tokens if usage else 0
        )

        return Result.ok(llm_resp)


        
    def close(self):
        self.__client.close()