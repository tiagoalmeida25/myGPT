# vertex pricing
# https://cloud.google.com/vertex-ai/docs/generative-ai/pricing?hl=pt-br#example_cost_calculation


from google.cloud import imagen_v2
import requests

import streamlit as st

import json
import google.generativeai as genai

with open("/Users/tiagoalmeida/Development/keys/gemini_api_key.json", "r") as f:
    data = json.load(f)
    genai.configure(api_key=data["api_key"])

class State:
    def __init__(self):
        self.user_input = ""
        # self.selected_model = list(models.keys())[0]
        # self.size = list(models[self.selected_model].keys())[0]
        self.price = 0
        self.image_url = ""


class StateDependencies:
    def __init__(self, state):
        self.state = state


class ImageGenerationSectionState(State):
    def __init__(self):
        super().__init__()
        self.dependencies = StateDependencies(self)

    # def get_models(self):
    #     return models.keys()

    # def get_sizes(self):
    #     return models[self.selected_model].keys()

    # def get_price(self):
    #     return models[self.selected_model][self.size]

    def get_state(self):
        return self


class ImageGenerationSection:
    def __init__(self, state: ImageGenerationSectionState):
        self.state = state
        self.model = imagen_v2.ImageClient()

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

                response = self.model.generate_image(
                    request={
                        "prompt": self.state.user_input,
                        "image_size": {"width": 512, "height": 512},
                        "num_images": 1,
                    }
                )

                for image in response.images:
                    self.state.image_url = image.uri

        if st.session_state.bt__generate:
            st.image(self.state.image_url, caption=user_input)

            st.download_button(
                label="Download Image",
                data=requests.get(self.state.image_url).content,
                file_name=f"{user_input}.jpg",
                mime="image/jpg",
            )


if __name__ == "__main__":
    state = ImageGenerationSectionState()
    section = ImageGenerationSection(state)
    section.run()
