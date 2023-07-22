"""Define LLM prompts focused on generating code to transform one csv format to another."""

CODE_CSV_MAPPING = (
    "INSTRUCTION:\n"
    "Your task is to produce a method in Python that will transform a CSV file into a new format. "
    "You will be provided with a MAPPING that describes how to transform the file. "
    "The MAPPING is a list of JSON objects where each JSON represents a column in the original table. "
    "If the 'target_name' field in the column description is 'null', that column should be dropped. "
    "The method you produce should a accept a string-formatted CSV as input and return a string-formatted CSV in the format specified in the provided MAPPING."
)