"""Methods for calling OpenAI APIs."""
from prompts.describe import DESCRIBE_CSV_FORMAT
from prompts.map import GENERATE_CSV_MAPPING
from prompts.code import CODE_CSV_MAPPING
from typing import Text, List
from enum import Enum
import logging
import openai
import os

OPENAI_TOKEN = os.getenv("OPENAI_API_KEY", "")
TEMPERATURE = 0.0
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
openai.api_key = OPENAI_TOKEN


class GPTMessageRole(str, Enum):
    """Enumerate possible speaker roles for a chat message."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class GPTMessage():
    """A single message in GPT chat history."""

    def __init__(self, role: GPTMessageRole, content: Text):
        """Initialize a GPT message object with speaker role and content."""
        self.role = role
        self.content = content

    def to_dict(self):
        """Return role and content in OpenAI format."""
        return {"role": self.role.value, "content": self.content}


class TableTransformer():
    """Class for converting one table format to another target format."""

    def __init__(
        self,
        content_table: Text,
        target_table: Text,
        temperature: float = TEMPERATURE
    ):
        """Initialize LLM table transformer class."""
        self.content = content_table
        self.target = target_table
        self.temperature = temperature
        self.model = "gpt-3.5-turbo-0613"

        self.original_description = None
        self.target_description = None

        self.table_mapping = None

        self.transform_method = None

    async def get_original_description(self):
        """Prompt LLM for description of the original table."""
        logger.info("Requesting description for original table...")
        self.original_description = await self._get_table_description(self.content)
        return self.original_description

    async def get_target_description(self):
        """Prompt LLM for description of the original table."""
        logger.info("Requesting description for original table...")
        self.target_description = await self._get_table_description(self.target)
        return self.target_description

    async def _get_table_description(self, table):
        table_description = await self._query_chat_gpt(messages=[
            GPTMessage(
                role=GPTMessageRole.SYSTEM,
                content=DESCRIBE_CSV_FORMAT
            ),
            GPTMessage(
                role=GPTMessageRole.USER,
                content=f"CSV:\n{table}\n\nRESPONSE:"
            )
        ])
        return self._get_gpt_response_content(table_description)

    async def get_table_mapping(self):
        """Given a original and target descriptions, prompt LLM to output a mapping."""
        logger.info("Requesting table mapping...")
        table_mapping = await self._query_chat_gpt(messages=[
            GPTMessage(
                role=GPTMessageRole.SYSTEM,
                content=GENERATE_CSV_MAPPING
            ),
            GPTMessage(
                role=GPTMessageRole.USER,
                content=(
                    f"ORIGINAL DESCRIPTION:\n{self.original_description}\n\n"
                    f"TARGET DESCRIPTION:\n{self.target_description}\n\n"
                    "RESPONSE:\n"
                )
            )
        ])
        self.table_mapping = self._get_gpt_response_content(table_mapping)
        return self.table_mapping

    async def get_transformation_code(self):
        """Given a mapping description, prompt the LLM to produce a method to transform the CSV."""
        logger.info("Requesting table transformation method...")
        table_mapping = await self._query_chat_gpt(messages=[
            GPTMessage(
                role=GPTMessageRole.SYSTEM,
                content=CODE_CSV_MAPPING
            ),
            GPTMessage(
                role=GPTMessageRole.USER,
                content=(
                    f"MAPPING:\n{self.table_mapping}\n\n"
                    "RESPONSE:\n"
                )
            )
        ])
        self.transform_method = self._get_gpt_response_content(table_mapping)
        return self.transform_method

    @staticmethod
    def _get_gpt_response_content(gpt_response) -> Text:
        """Validate and return the response content from a GPT response dict."""
        logger.debug(f"Validating and formatting gpt response: {gpt_response}")
        if isinstance(gpt_response, dict):
            choices = gpt_response.get("choices")
            if isinstance(choices, list) and len(choices) > 0:
                result = choices[0]
                if isinstance(result, dict):
                    return result.get("message", {}).get("content", "")
        logger.warning(f"Failed to validate GPT response: {gpt_response}")
        return ""

    async def _query_chat_gpt(self, messages: List[GPTMessage]):
        """Query openai ChatCompletion endpoint."""
        # NOTE: I use ChatGPT instead of GPT3/4 here because I think it will
        # perform just as well and its 10x cheaper :)
        logger.debug(f"Submitting ChatGPT request with prompt: {messages}")
        return await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[m.to_dict() for m in messages],
            temperature=self.temperature,
            request_timeout=60,
        )
