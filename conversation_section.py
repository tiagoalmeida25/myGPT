from abc import ABC
import streamlit as st
import openai
import os
import pickle

from typing import Generic, TypeVar

T = TypeVar("T")

openai.api_key = "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"


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
            # If not exist, then start a new list for saving conversations
            self.state.conversations = []

        st.title("Conversation Mode")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text("")
            if st.button("Clear Conversation"):
                # Clear the conversation list and delete the pickle file
                self.state.conversations = []
                os.remove("conversations.pkl")
                st.info("Conversation cleared!")
        with col2:
            selected_model = st.selectbox(
                "Select a model", ["gpt-3.5-turbo-1106", "gpt-4-1106-preview"]
            )
        with st.expander("Pricing"):
            st.dataframe(
                hide_index=True,
                data=[
                    ["Model", "Input", "Output"],
                    ["gpt-3.5-turbo-1106", "	$0.0010 / 1K tokens", "$0.0020 / 1K tokens"],
                    ["gpt-4-1106-preview", "$0.0010 / 1K tokens", "$0.0020 / 1K tokens"],
                ],
            )

        # Display previous conversations
        for conversation in self.state.conversations:
            st.markdown(f"**User:** {conversation['user']}")
            st.markdown(f"**Assistant:** {conversation['assistant']}")

        # Input field
        user_input = st.text_input("Enter your message")

        # Submit button
        if st.button("Submit"):
            # Send the user's message to OpenAI API
            response = openai.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{user_input}"},
                ],
            )

            assistant_response = response.choices[0].message.content

            # Save the conversation
            self.state.conversations.append(
                {"user": user_input, "assistant": assistant_response}
            )
            with open("conversations.pkl", "wb") as f:
                pickle.dump(self.state.conversations, f)

            # Display the response
            st.markdown(f"**Assistant:** {assistant_response}")
