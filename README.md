# LLMTableTransformation

View app here: https://llmtabletransformation-ejfa6u1s2m8.streamlit.app/ !

## Task Description
In the financial sector, one of the routine tasks is mapping data from various sources in Excel tables. For example, a company may have a target format for employee health insurance tables (Template) and may receive tables from other departments with essentially the same information, but with different column names, different value formats, and duplicate or irrelevant columns.
Your task is to devise an approach using LLM for mapping tables A and B to the template by transferring values and transforming values into the target format of the Template table (example below)

## Example user journey:
- The user uploads the Template table.
- The user uploads table A.
- For each column in the Template, the system suggests columns from column A (1 or more relevant candidates), showing the basis for the decision (formats, distributions, and other features that are highlighted in the backend).
- The person confirms the mapping.
- Next, the data transformation stage begins. The system generates and displays the code with which it will perform the transformation. The user can edit it and run it, checking the correctness of the mapping.
- At the output, the user receives a table in the Template format (columns, value formats) but with values from table A.
- The same for table B.

## Implementation
I implemented this application using Streamlit as the frontend and the OpenAI client with ChatGPT as the LLM model to support the functionality.

To get started the user should:
1. Click the upload widget on the left-hand-side to upload the original/contentful CSV file from their computer
2. Click the upload widget on the right-hand-side to upload the target template CSV file from their computer

As soon as both CSV files are uploaded, processing will automatically start. There are three tabs below the upload widgets: `Description`, `Mapping`, and `Code`. Each tab shows output displayed by the LLM.

### Description
The description tab will show a description of the format of each CSV file formatted as a list of dictionaries. Each dictionary in the list represents one column in the original CSV and provides the following information:
- Column name
- Data type
- Data format
- Representative example
- Written description

// NOTE: I think for a final version of the app, we don't really need to description tab, and could combine the description/mapping prompts into a single prompt. I kept the separate description tab in this version for two reasons: 1) I think it helps show the user what's going on internally so the whole process is more clear, and 2) I think the task specification said the app should output a description of the input CSVs 

### Mapping
This tab contains an LLM-produces mapping of the original CSV to the target format. It is output as a list of JSON objects, where each dictionary represents a column in the original CSV file and contains information about the original format and the target format:
- Original/target column name
- Original/target data type
- Original/target data format
- Original/target example
- Confidence score

If the original column has no predicted mapping in the target CSV, `target_name` will simply be output as `null`.

The confidence score field can be used to gauge whether or not the system should ask for human verification of the mapping for that field (not implemented yet).

### Code
The final tab contains LLM-produced Python code that will map the original table to the target table format.
The method produced should a accept a string-formatted CSV as input and return a string-formatted CSV in the format specified in the mapping tab.

## Notes

### Work in Progress
Based on the project specifications, the app is currently ~85-90% complete. With more time, I would implement the following:
- Add a human-review step to the mapping page. My plan is to turn the mapping page into a form where each column from the original table has a drop-down with column names from the target format
- Use confidence scores from mapping output to require human review on non-confident mappings
- Validate the mapping output for obvious mistakes: ex/ two columns from the input table cannot be mapped to a single column in the output table
- Run the original CSV through the outputted code and display the result in the target format
- Download button for outputted CSV and/or generated Python script
- Download/upload buttons for the sample files make testing easier

### Edge Cases
- Malformed data:
    - Duplicate column names
    - Missing column names
    - Rows contain varying number of values (ex/ there are 10 columns, but a particular row only has 8 values)
    - Missing/incorrect quotations and/or escape chars. (ex/ If a string value has a comma in it, the string must be wrapped in quotations)
- Nothing mapped to target column: I handled the case where an original column has no corresponding column in the output, however I didn't specify what to do if a column in the target format has nothing mapped to it. The result should be that the column name is included, but all the values are `null`.