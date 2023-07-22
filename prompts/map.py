"""Define LLM prompts focused on mapping one csv format to another."""

GENERATE_CSV_MAPPING = (
    "INSTRUCTION:\n"
    "You will be provided with two descriptions of CSV file formats: an ORIGINAL and TARGET. "
    "Each CSV file format is a list of JSON object, where each JSON object represents a column in the csv table. "
    "Each column description includes: column name, column type, data format, representative example, and written description. "
    "For each column in the ORIGINAL description, do the following:\n"
    "Determine if there is a corresponding column in the TARGET description.\n"
    "Provide a confidence score between 0 and 1 for the mapping.\n"
    "If a corresponding column is identified, provide the following information:\n"
    "- The original column name and the target column name\n"
    "- The orginal data type and the target data type\n"
    "- The orginal data format and the target data format\n"
    "- A representative example from both the original and target tables\n"
    "If no corresponding column exists in the TARGET description, simply provide the target name as null.\n"
    "Output results as a list of JSON objects where each item in the list represents a column in the ORIGINAL table, as show in the EXAMPLE RESPONSE.\n\n"
    "EXAMPLE ORIGINAL CSV DESCRIPTION:\n"
    '[{"name":"Date_of_Policy", "type":"str", "format":"mm/dd/yyyy", "example":"05/01/2023", "description":"The Date_of_Policy column contains date strings formatted as mm/dd/yyyy."},'
    '{"name":"FullName", "type":"str", "format":"First Last", "example":"John Doe", "description":"The FullName column contains full names formatted as First Last."},'
    '{"name":"PolicyNum", "type":"int", "format":00000, "example":38208, "description":"The PolicyNum column contains the client policy number as a 5-digit integer."}]\n\n'
    "EXAMPLE TARGET CSV DESCRIPTION:\n"
    '[{"name":"Date", "type":"str", "format":"mm-dd-yyyy", "example":"12-05-1995", "description":"The Date column contains date strings formatted as mm-dd-yyyy."},'
    '{"name":"Policy_Number", "type":"str", "format":"00000", "example":"27204", "description":"The Policy_Number column contains the client policy number as a 5-digit string."}]\n\n'
    "EXAMPLE RESPONSE:\n"
    '[{"original_name":"Date_of_Policy", "target_name":"Date", "original_type":"str", "target_type":"str", "original_format":"mm/dd/yyyy", "target_type":"mm-dd-yyyy", "original_example":"05/01/2023", "target_example":"12-05-1995", "confidence":0.80},'
    '{"original_name":"FullName", "target_name": null, "confidence":0.99},'
    '{"original_name":"PolicyNum", "target_name":"Policy_Number", "original_type":"int", "target_type":"str", "original_format":00000, "target_format":"00000", "original_example":38208, "target_example":"27204", "confidence":0.90}]\n\n'
)
