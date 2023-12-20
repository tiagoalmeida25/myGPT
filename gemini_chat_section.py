import streamlit as st

import json
import google.generativeai as genai


genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# with open("/Users/tiagoalmeida/Development/keys/gemini_api_key.json", "r") as f:
#     data = json.load(f)
#     genai.configure(api_key=data["api_key"])


class State:
    def __init__(self):
        self.chat = None
        self.gemini_conversations = []
        self.user_input = ""
        self.assistant_response = ""

    def start_chat(self):
        self.chat = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=genai.GenerationConfig(temperature=0.8),
        )

    def save_state(self):
        with open("gemini_conversations.json", "w") as f:
            json.dump(self.gemini_conversations, f)

    def clear_state(self):
        self.gemini_conversations = []
        self.user_input = ""
        self.assistant_response = ""
        self.start_chat()
        self.save_state()

    def get_gemini_conversations(self):
        if "gemini_conversations" not in st.session_state:
            self.gemini_conversations = self.dependencies.open_gemini_conversations()
        return self.gemini_conversations

    def update_conversation(self, user_input, assistant_response):
        self.gemini_conversations.append({"user": user_input, "assistant": assistant_response})
        with open("gemini_conversations.json", "w") as f:
            json.dump(self.gemini_conversations, f)


class StateDependencies:
    def __init__(self, state):
        self.state = state

    def open_gemini_conversations(self):
        try:
            with open("gemini_conversations.json", "r") as f:
                model_gemini_conversations_dict = json.load(f)
        except:
            model_gemini_conversations_dict = []
        return model_gemini_conversations_dict


class GeminiChatState(State):
    def __init__(self):
        super().__init__()
        self.dependencies = StateDependencies(self)

    def get_user_input(self):
        if "user_input" not in st.session_state:
            self.user_input = ""
        return self.user_input

    def get_assistant_response(self):
        if "assistant_response" not in st.session_state:
            self.assistant_response = ""
        return self.assistant_response

    def get_state(self):
        return self


class GeminiChatSection:
    def __init__(self, state: GeminiChatState):
        self.state = state
        self.state.start_chat()

    def run(self):
        st.title("Code Chat")
        for conversation in self.state.get_gemini_conversations():
            st.markdown(f"**User:** {conversation['user']}")
            st.markdown(f"**Assistant:** {conversation['assistant']}")

        self.state.user_input = st.text_input(
            "Enter your message", value=self.state.user_input
        )

        col1, _, col2 = st.columns([1, 2, 1])

        with col1:
            if st.button("Submit", use_container_width=True):
                response = self.state.chat.generate_content(self.state.user_input)

                self.state.assistant_response = response.text

                self.state.update_conversation(
                    self.state.user_input, self.state.assistant_response
                )

        if self.state.assistant_response != "":
            st.markdown(f"**Assistant:** {self.state.assistant_response}")

            self.state.user_input = ""
            self.state.assistant_response = ""

        with col2:
            if st.button("Clear Conversation", use_container_width=True):
                self.state.clear_state()
