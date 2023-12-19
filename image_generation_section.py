from abc import ABC
import streamlit as st
import openai

from typing import Generic, TypeVar

T = TypeVar("T")

openai.api_key = "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"


class Section(Generic[T], ABC):
    pass


class State(ABC):
    pass


class StateDependencies(ABC):
    pass


class ImageGenerationSectionState(StateDependencies):
    def get_state():
        return ImageGenerationSectionState()

    def __init__(self):
        pass

    def save_state(self):
        pass

    def clear_state(self):
        pass


class ImageGenerationSection(Section[ImageGenerationSectionState]):
    def __init__(self, state: ImageGenerationSectionState):
        self.state = state

    def run(self):
        st.title("Image Generation")

        col1, col2, col3 = st.columns(3)

        with col1:
            selected_model = st.selectbox(
                "Select a model",
                ["dall-e-2", "dall-e-3"],
            )
        with col2:
            if selected_model == "dall-e-2":
                selected_size = st.selectbox(
                    "Select a size",
                    ["512x512", "1024x1024"],
                )
            else:
                selected_size = st.selectbox(
                    "Select a size",
                    ["1024x1024"],
                )

        with st.expander("Pricing"):
            st.dataframe(
                hide_index=True,
                data=[
                    ["Model", "Size", "Price"],
                    ["DALL·E 3", "1024x1024", "$0.040 / image"],
                    ["DALL·E 2", "1024x1024", "$0.020 / image"],
                    ["", "512x512", "$0.018 / image"],
                ]
            )
            
        # Input field
        user_input = st.text_input("Enter your prompt")

        # Submit button
        if st.button("Submit"):
            response = openai.images.generate(
                model=selected_model,
                prompt=user_input,
                size=selected_size,
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url

            # Display the response
            st.image(image_url)

            if st.button("Save Image"):
                if response.status_code == 200:
                    with open(f"{user_input}.jpg", "wb") as file:
                        file.write(image_url)
