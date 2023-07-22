"""Main streamlit app for table transform project."""
from llm_utils import TableTransformer
import streamlit as st
import logging
import asyncio
import json

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ORIGINAL = None
TARGET = None


def _format_json(json_string):
    """Format json string to json object."""
    try:
        return json.loads(json_string)
    except Exception:
        try:
            return eval(json_string)
        except Exception:
            logger.warning(f"Failed to parse json: {json_string}")
            return json_string


async def display_original_upload():
    """Display upload widget for original CSV."""
    st.subheader("Upload Original CSV")
    try:
        original = st.file_uploader("Original CSV")
        if original:
            logger.info(f"Uploading data file {original.name}...")
            return original.read().decode("utf-8")
    except Exception as e:
        st.error(f"Failed to upload data file! {e}")
        logger.error(f"Failed to upload data file! {e}")


async def display_template_upload():
    """Display upload widget for template CSV."""
    st.subheader("Upload Target CSV Template")
    try:
        target = st.file_uploader("Target CSV")
        if target:
            logger.info(f"Uploading template file {target.name}...")
            return target.read().decode("utf-8")
    except Exception as e:
        st.error(f"Failed to upload template file! {e}")
        logger.error(f"Failed to upload template file! {e}")


async def display_table_descriptions(table_transformer):
    """Display LLM-generated table descriptions."""
    col1, col2 = st.columns(2)
    with st.spinner("Generating table descriptions..."):
        original_desc, target_desc = await asyncio.gather(
            table_transformer.get_original_description(),
            table_transformer.get_target_description()
        )
        with col1:
            st.json(_format_json(original_desc))
        with col2:
            st.json(_format_json(target_desc))


async def display_table_mapping(table_transformer):
    """Display the table mapping."""
    with st.spinner("Generating table mapping..."):
        table_mapping = await table_transformer.get_table_mapping()
        st.json(_format_json(table_mapping))


async def display_transform_code(table_transformer):
    """Display LLM-produced code for table transformation."""
    with st.spinner("Generating table transformation code..."):
        tranformation_code = await table_transformer.get_transformation_code()
        st.code(tranformation_code, language="python", line_numbers=True)


async def run_app():
    """Run streamlit app."""
    # header and instructions
    st.header("LLM Table Transformation")
    st.text(
        """
        Upload a contentful csv file and template output csv file.
        The LLM will assist by verifying the mapping between the original and target formats,
        and then output code to perform the transformation.
        Upload your own file, or try it with a sample file.
        Processing will start once both files are uploaded.
        """
    )

    # File upload
    col1, col2 = st.columns(2)
    with col1:
        original = await display_original_upload()
    with col2:
        target = await display_template_upload()

    # define tabs
    description, mapping, code = st.tabs(["Description", "Mapping", "Code"])

    if original and target:
        table_transformer = TableTransformer(original, target)
        with description:
            await display_table_descriptions(table_transformer)
        with mapping:
            await display_table_mapping(table_transformer)
        with code:
            await display_transform_code(table_transformer)

        # mapping = await determine_table_mapping(original, target)


if __name__ == "__main__":
    st.set_page_config(
        page_title="LLM Table Transformation",
        layout="wide"
    )
    asyncio.run(run_app())
