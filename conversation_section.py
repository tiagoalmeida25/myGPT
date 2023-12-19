from abc import ABC
import streamlit as st
import openai

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
        self.state.conversations = []  # could use firebase to store conversations
        self.selected_model = "gpt-4-1106-preview"
        self.price = 0
        self.user_input = ""
        self.assistant_response = ""

    def run(self):
        st.title("Conversation Mode")

        col1, col2 = st.columns([1, 2])

        with col1:
            self.selected_model = st.selectbox(
                "Select a model",
                ["gpt-3.5-turbo-1106", "gpt-4-1106-preview"],
            )
        with col2:
            st.text("")
            if self.selected_model == "gpt-3.5-turbo-1106":
                st.info("Pricing: \$0.0010 / 1K tokens , $0.0020 / 1K tokens")
            if self.selected_model == "gpt-4-1106-preview":
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

        if self.assistant_response:
            st.markdown(f"**Assistant:** {self.assistant_response}")
            self.user_input = ""
            self.assistant_response = ""

        st.text_input("Enter your message", value=self.user_input)
        self.calculate_price()

        if self.price > 0:
            st.markdown(f"**Price:** ${self.price:.4f}")

        col1, _, col2 = st.columns([1, 2, 1])

        with col1:
            st.button("Submit", use_container_width=True, key="submit")

            if st.session_state.submit:
                response = openai.chat.completions.create(
                    model=self.selected_model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant. Some regards: When giving code as a response, no need to include comments, unless requested or strictly necessary.",
                        },
                        {"role": "user", "content": f"{self.user_input}"},
                    ],
                )

        if st.session_state.submit:
            self.assistant_response = response.choices[0].message.content

            self.state.conversations.append(
                {"user": self.user_input, "assistant": self.assistant_response}
            )

    def calculate_price(self):
        tokens = len(self.user_input.split(" ")) * 0.75

        if self.selected_model == "gpt-3.5-turbo-1106":
            self.price = 0.001 * tokens / 1000
        elif self.selected_model == "gpt-4-1106-preview":
            self.price = 0.01 * tokens / 1000
