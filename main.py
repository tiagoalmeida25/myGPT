import os
import pathlib
import sys
from copy import deepcopy

import streamlit as st

from conversation_section import ConversationSection, ConversationSectionState
from image_generation_section import ImageGenerationSection, ImageGenerationSectionState

st.set_page_config(layout="wide")


SECTION_STATE_MAP = {
    ConversationSection: ConversationSectionState,
    ImageGenerationSection: ImageGenerationSectionState,
}


def run_app():
    mapping = {
        "Conversation": ConversationSection,
        "Image Generation": ImageGenerationSection,
    }

    selected_section = st.sidebar.selectbox("Select a section:", list(mapping.keys()))

    sections = mapping.get(selected_section)

    state = SECTION_STATE_MAP[sections].get_state()
    section = sections(state)
    section.run()


if __name__ == "__main__":
    run_app()
