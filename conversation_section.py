import json
import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

# with open("/Users/tiagoalmeida/Development/keys/openai_api_key.json", "r") as f:
#     data = json.load(f)
#     openai.api_key = data["api_key"]

models = {
    "gpt-3.5-turbo-1106": {"input": 0.001, "output": 0.002},
    "gpt-4-1106-preview": {"input": 0.01, "output": 0.03},
}


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
        self.selected_model = list(models.keys())[0]
        self.price = models[self.selected_model]["input"]


class StateDependencies:
    def __init__(self, state):
        self.state = state


class ConversationSectionState(State):
    def __init__(self):
        super().__init__()
        self.dependencies = StateDependencies(self)

    def get_models(self):
        return models.keys()

    def get_price(self):
        return [
            models[self.selected_model]["input"],
            models[self.selected_model]["output"],
        ]

    def get_conversations(self):
        try:
            with open("conversations.json", "r") as f:
                model_conversations_dict = json.load(f)
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
        self.save_state()

    def get_state(self):
        return self


class ConversationSection:
    def __init__(self, state: ConversationSectionState):
        self.state = state

    def run(self):
        st.title("Conversation Mode")

        col1, col2 = st.columns([1, 2])

        with col1:
            self.state.selected_model = st.selectbox(
                "Select a model", options=self.state.get_models()
            )

        with col2:
            st.text("")
            prices = self.state.get_price()
            st.info(f"Pricing: \${prices[0]} / 1K tokens , ${prices[1]} / 1K tokens")

        for conversation in self.state.get_conversations():
            if conversation["role"] == "user":
                st.markdown(f"**User:** {conversation['content']}")
            elif conversation["role"] == "assistant":
                st.markdown(f"**Assistant:** {conversation['content']}")

        self.state.user_input = st.text_input(
            "Enter your message", value=self.state.user_input
        )

        if self.state.user_input != "":
            st.markdown(f"**Price:** ${self.calculate_price():.6f}")

        col1, _, col2 = st.columns([1, 2, 1])

        with col1:
            st.button("Send", use_container_width=True, key="send")

            if st.session_state.send:
                self.state.conversations = self.state.get_conversations()
                self.state.conversations.append(
                    {
                        "role": "user",
                        "content": self.state.user_input,
                    }
                )

                response = openai.chat.completions.create(
                    model=self.state.selected_model,
                    messages=self.state.conversations,
                )

                self.state.assistant_response = response.choices[0].message.content

                self.state.conversations.append(
                    {
                        "role": "assistant",
                        "content": self.state.assistant_response,
                    },
                )
                self.state.save_state(self.state.conversations)

        with col2:
            if st.button("Clear", use_container_width=True):
                self.state.clear_state()

        if self.state.assistant_response != "":
            st.markdown(f"**Assistant:** {self.state.assistant_response}")
            self.state.user_input = ""
            self.state.assistant_response = ""

    def calculate_price(self):
        tokens = len(self.state.user_input.split(" ")) * 0.75

        return self.state.get_price()[0] * tokens / 1000
