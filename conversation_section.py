from abc import ABC
import streamlit as st
import openai
import os
import pickle

from typing import Generic, TypeVar

T = TypeVar("T")

openai.api_key = st.secrets["OPENAI_API_KEY"]


class Section(Generic[T], ABC):
    pass


class State(ABC):
    pass


class StateDependencies(ABC):
    pass


class ConversationSectionState(StateDependencies):
    conversations = State()

    def get_state():
        return ConversationSectionState()

    def __init__(self):
        self.conversations = ConversationSectionState.conversations

    def save_state(self):
        ConversationSectionState.conversations = self.conversations

    def clear_state(self):
        ConversationSectionState.conversations = State()
        ConversationSectionState.conversations.save_state()


class ConversationSection(Section[ConversationSectionState]):
    def __init__(self, state: ConversationSectionState):
        self.state = state

    def run(self):
        # Check if the pickle file for saving conversations exists
        if os.path.isfile("conversations.pkl"):
            # If exists, then load the previous conversations
            with open("conversations.pkl", "rb") as f:
                self.state.conversations = pickle.load(f)
        else:
            self.state.conversations = []

        st.title("Conversation Mode")

        col1, col2 = st.columns([1, 2])

        with col1:
            selected_model = st.selectbox(
                "Select a model", ["gpt-3.5-turbo-1106", "gpt-4-1106-preview"]
            )
        with col2:
            st.text("")
            if selected_model == "gpt-3.5-turbo-1106":
                st.info("Pricing: \$0.0010 / 1K tokens , $0.0020 / 1K tokens")
            if selected_model == "gpt-4-1106-preview":
                st.info("Pricing: \$0.010 / 1K tokens , $0.030 / 1K tokens")

        with st.expander("See pricing details", expanded=False):
            st.markdown(
                """
                    Multiple models, each with different capabilities and price points. 
                    Prices are per 1,000 tokens. You can think of tokens as pieces of words, 
                    where 1,000 tokens are about 750 words. This paragraph is 35 tokens. ~ \$0.00035 
                """
            )

        # Display previous conversations
        for conversation in self.state.conversations:
            st.markdown(f"**User:** {conversation['user']}")
            st.markdown(f"**Assistant:** {conversation['assistant']}")

        user_input = st.text_input("Enter your message")

        col1, _, col2 = st.columns([1, 2, 1])

        with col1:
            submit = st.button("Submit", use_container_width=True)
            if submit:
                response = openai.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"{user_input}"},
                    ],
                )

        if submit:
            user_input = ''
            assistant_response = response.choices[0].message.content

            self.state.conversations.append(
                {"user": user_input, "assistant": assistant_response}
            )
            with open("conversations.pkl", "wb") as f:
                pickle.dump(self.state.conversations, f)

            st.markdown(f"**Assistant:** {assistant_response}")

        if self.state.conversations != []:
            with col2:
                if st.button("Clear Conversation", use_container_width=True):
                    # Clear the conversation list and delete the pickle file
                    self.state.conversations = []
                    os.remove("conversations.pkl")
                    st.info("Conversation cleared!")
