from prompts.describe import DESCRIBE_CSV_FORMAT
import openai
import os

openai.api_key(os.getenv("OPENAI_API_KEY"))


class TableTransformer():

    def __init__(self, content_table, template_table):
        self.content = content_table
        self.template = template_table

async def get_table_description(table):
    return table
