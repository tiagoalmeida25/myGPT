import streamlit as st

from conversation_section import ConversationSection, ConversationSectionState
from image_generation_section import ImageGenerationSection, ImageGenerationSectionState

st.set_page_config(layout="wide")


SECTION_STATE_MAP = {
    ConversationSection: ConversationSectionState,
    ImageGenerationSection: ImageGenerationSectionState,
}


def run_app():
    st.sidebar.title("myGPT")
    if "isLoggedIn" not in st.session_state:
        st.session_state.isLoggedIn = False

    login_placeholder = st.container()

    if not st.session_state.isLoggedIn:
        with login_placeholder:
            st.header("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login"):
                if username == "tiagoalmeida" and password == "themaker":
                    st.success("Logged in as tiagoalmeida")
                    st.session_state.isLoggedIn = True
                    login_placeholder = None
                    
                elif username == "margaridaoliveira" and password == "thebelicious":
                    st.success("Logged in as margaridaoliveira")
                    st.session_state.isLoggedIn = True
                    login_placeholder = None
                    
                else:
                    st.error("Incorrect username or password")

    if st.session_state.isLoggedIn:
        login_placeholder = None
        mapping = {
            "Conversation": ConversationSection,
            "Image Generation": ImageGenerationSection,
        }

        selected_section = st.sidebar.selectbox(
            "Select a section:", list(mapping.keys())
        )

        sections = mapping.get(selected_section)

        state = SECTION_STATE_MAP[sections].get_state()
        section = sections(state)
        section.run()


if __name__ == "__main__":
    run_app()
