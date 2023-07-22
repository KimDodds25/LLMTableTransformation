from llm_utils import get_table_description
import streamlit as st
import logging
import asyncio

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ORIGINAL = None
TARGET = None


async def display_original_upload():
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
    st.subheader("Upload Target CSV Template")
    try:
        target = st.file_uploader("Target CSV")
        if target:
            logger.info(f"Uploading template file {target.name}...")
            return target.read().decode("utf-8")
    except Exception as e:
        st.error(f"Failed to upload template file! {e}")
        logger.error(f"Failed to upload template file! {e}")


async def display_table_descriptions(original, target):
    col1, col2 = st.columns(2)
    with col1:
        original_desc = await get_table_description(original)
        st.text(original_desc)
    with col2:
        target_desc = await get_table_description(target)
        st.text(target_desc)


async def determine_table_mapping(original_data, target_data):
    pass


async def run_app():
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

    col1, col2 = st.columns(2)
    with col1:
        original = await display_original_upload()
    with col2:
        target = await display_template_upload()

    description, = st.tabs(["Description"])
    with description:
        await display_table_descriptions(original, target)

        #mapping = await determine_table_mapping(original, target)


if __name__ == "__main__":
    st.set_page_config(
        page_title="LLM Table Transformation",
        layout="wide"
    )
    asyncio.run(run_app())
