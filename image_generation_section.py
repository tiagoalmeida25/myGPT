import json
import requests
import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

# with open("/Users/tiagoalmeida/Development/keys/openai_api_key.json", "r") as f:
#     data = json.load(f)
#     openai.api_key = data["api_key"]

models = {
    "dall-e-2": {"512x512": 0.018, "1024x1024": 0.020},
    "dall-e-3": {"1024x1024": 0.040},
}


class State:
    def __init__(self):
        self.user_input = ""
        self.selected_model = list(models.keys())[0]
        self.size = list(models[self.selected_model].keys())[0]
        self.price = 0
        self.image_url = ""


class StateDependencies:
    def __init__(self, state):
        self.state = state


class ImageGenerationSectionState(State):
    def __init__(self):
        super().__init__()
        self.dependencies = StateDependencies(self)

    def get_models(self):
        return models.keys()

    def get_sizes(self):
        return models[self.selected_model].keys()

    def get_price(self):
        return models[self.selected_model][self.size]

    def get_state(self):
        return self


class ImageGenerationSection:
    def __init__(self, state: ImageGenerationSectionState):
        self.state = state

    def run(self):
        st.title("Image Generation")

        col1, col2, col3 = st.columns(3)

        with col1:
            self.state.selected_model = st.selectbox(
                "Select a model",
                self.state.get_models(),
            )
        with col2:
            self.state.size = st.selectbox(
                "Select a size",
                self.state.get_sizes(),
            )

        with col3:
            st.text("")
            st.info(f"Pricing: ${self.state.get_price()}/ image")

        user_input = st.text_input("Enter your prompt")

        col1, _ = st.columns([1, 3])
        with col1:
            st.button("Generate", use_container_width=True, key="bt__generate")

            if st.session_state.bt__generate:
                self.state.image_url = ""

                response = openai.images.generate(
                    model=self.state.selected_model,
                    prompt=user_input,
                    size=self.state.size,
                    quality="standard",
                    n=1,
                )

                self.state.image_url = response.data[0].url

        if st.session_state.bt__generate:
            st.image(self.state.image_url, caption=user_input)

            st.download_button(
                label="Download Image",
                data=requests.get(self.state.image_url).content,
                file_name=f"{user_input}.jpg",
                mime="image/jpg",
            )
