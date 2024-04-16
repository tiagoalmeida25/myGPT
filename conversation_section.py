import json
import ollama
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import textwrap

models = [
    "mistral",
    "codellama",
]


class State:
    def __init__(self):
        self.user_input = ""
        self.assistant_response = ""
        self.conversations = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Some regards: When giving code as a response, no need to include comments, unless requested or strictly necessary.",
            },
        ]
        self.selected_model = models


class StateDependencies:
    def __init__(self, state):
        self.state = state


class ConversationSectionState(State):
    def __init__(self):
        super().__init__()
        self.dependencies = StateDependencies(self)

    def get_models(self):
        return models

    def get_conversations(self):
        try:
            with open("conversations.json", "r") as f:
                model_conversations_dict = json.load(f)

            for conversation in model_conversations_dict:
                conversation["content"] = textwrap.fill(conversation["content"], width=30)
            print(model_conversations_dict)
        except:
            model_conversations_dict = []

        return model_conversations_dict

    def save_state(self, conversations):
        with open("conversations.json", "w") as f:
            json.dump(conversations, f)

    def clear_state(self):
        self.conversations = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Some regards: When giving code as a response, no need to include comments, unless requested or strictly necessary.",
            },
        ]
        self.user_input = ""
        self.assistant_response = ""
        self.save_state(self.conversations)

    def get_state(self):
        return self


class ConversationSection:
    def __init__(self, state: ConversationSectionState):
        self.state = state

    def run(self):
        st.title("Personal Chat")

        self.state.selected_model = st.selectbox("Select a model", options=self.state.get_models(), on_change=self.state.clear_state)

        for i, conversation in enumerate(self.state.get_conversations()):
            cols = st.columns([1, 49])
            if conversation["role"] == "user":
                with cols[0]:
                    st.markdown(":smile:")
                with cols[1]:
                    with stylable_container(
                        key=f"user_{i}",
                        css_styles="""
                        {
                            background-color: #171A21;
                            color: white;
                            border-radius: 8px;
                            padding-top: 8px;
                            padding-bottom: 8px;
                            padding-left: 16px;
                            padding-right: 16px;
                            overflow-wrap: break-word;
                            hyphens: auto;
                        }
                        """,
                    ):
                        st.markdown(f"{conversation['content']}")
            elif conversation["role"] == "assistant":
                with cols[0]:
                    st.markdown(":robot_face:")
                with cols[1]:

                    with stylable_container(
                        key=f"user_{i}",
                        css_styles="""
                        {
                            background-color: #1A1C24;
                            color: white;
                            border-radius: 8px;
                            padding-top: 8px;
                            padding-bottom: 8px;
                            padding-left: 16px;
                            padding-right: 16px;
                        }
                        """,
                    ):
                        st.markdown(f"{conversation['content']}")

        self.state.user_input = st.text_area("How can I help you", value=self.state.user_input)

        col1, _, col2 = st.columns([1, 2, 1])

        with col1:
            st.button("Send", use_container_width=True, key="send", on_click=lambda: setattr(self.state, "send", True))

            if st.session_state.send:
                self.state.conversations = self.state.get_conversations()
                self.state.conversations.append(
                    {
                        "role": "user",
                        "content": self.state.user_input,
                    }
                )

                response = ollama.chat(
                    model=self.state.selected_model,
                    messages=self.state.conversations,
                    stream=False,
                )

                self.state.assistant_response = response["message"]["content"]

                self.state.conversations.append(
                    {
                        "role": "assistant",
                        "content": self.state.assistant_response,
                    },
                )
                self.state.save_state(self.state.conversations)

        with col2:
            if st.button("Clear", use_container_width=True, key="clear", on_click=lambda: setattr(self.state, "clear", True)):
                self.state.clear_state()

        if self.state.assistant_response != "":
            self.state.user_input = ""
            self.state.assistant_response = ""
            st.experimental_rerun()
