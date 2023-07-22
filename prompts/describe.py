DESCRIBE_CSV_FORMAT = (
    "INSTRUCTION:\n"
    "You will be provided with a csv-formatted string. "
    "For each column in the csv do the following:\n"
    "Identify the name of the column.\n"
    "Identify the type of data stored in the column.\n"
    "Identify the format of the data in the column.\n"
    "Provide one representative example from the column.\n"
    "Provide a written description of the column and its contents."
    "Output results as a list of JSON objects as show in the EXAMPLE.\n\n"
    "EXAMPLE CSV:\n"
    "Date,Name,PolicyNum\n"
    "01-05-2023,John D.,12345"
    "02-05-2023,Jane S.,67890"
    "03-05-2023,Michael B.,10111\n\n"
    "EXAMPLE_RESPONSE:\n"
    '[{"name": "Date", "type": "str", "format": "mm-dd-yyyy", "example": "01-05-2023", "description": "The Date column contains date strings formatted with zero-padding as mm-dd-yyyy"},'
    '{"name": "Name", "type": "str", "format": "First L.", "example": "John D.", "description": "The Name column contains names formatted as the full first name with the last initial followed by a period."},'
    '{"name": "PolicyNum", "type": "int", "format": "00000", "example": "12345", "description": "The PolicyNum column contains policy numbers formatted as a 5-digit integer."}]'
)