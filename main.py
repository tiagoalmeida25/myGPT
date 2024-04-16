import streamlit as st

from conversation_section import ConversationSection, ConversationSectionState
# from code_chat_section import CodeChatSection, CodeChatState
# from image_generation_section import ImageGenerationSection, ImageGenerationSectionState
# from gemini_chat_section import GeminiChatSection, GeminiChatState

st.set_page_config(layout="wide")


SECTION_STATE_MAP = {
    ConversationSection: ConversationSectionState,
    # CodeChatSection: CodeChatState,
    # ImageGenerationSection: ImageGenerationSectionState,
    # GeminiChatSection: GeminiChatState,
}


def run_app():
    # st.sidebar.title("myGPT")

    mapping = {
        "Conversation": ConversationSection,
        # "Code Chat": CodeChatSection,
        # "Image Generation": ImageGenerationSection,
        # "Gemini Chat": GeminiChatSection,
    }

    # selected_section = st.sidebar.selectbox(
    #     "Select a section:", list(mapping.keys())
    # )

    sections = mapping.get(list(mapping.keys())[0])

    state_instance = SECTION_STATE_MAP[sections]()
    state = state_instance.get_state()
    section = sections(state)
    section.run()


if __name__ == "__main__":
    run_app()
