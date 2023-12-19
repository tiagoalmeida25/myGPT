import streamlit as st
from abc import ABC
from typing import Generic, TypeVar

T = TypeVar("T")


class Section(Generic[T], ABC):
    pass


class State(ABC):
    pass


class StateDependencies(ABC):
    pass


class HomeSectionState(StateDependencies):
    selected_section = State()

    @st.cache(allow_output_mutation=True)
    def get_state():
        return HomeSectionState()

    def __init__(self):
        self.selected_section = HomeSectionState.selected_section

    def save_state(self):
        HomeSectionState.selected_section = self.selected_section

    def clear_state(self):
        HomeSectionState.selected_section = State()
        HomeSectionState.selected_section.save_state()


class HomeSection(Section[HomeSectionState]):
    def __init__(self, state: HomeSectionState):
        self.state = state

    def run(self):
        st.title("Home Page")

        sections = ["Section 1", "Section 2", "Section 3"]
        self.state.selected_section = st.selectbox("Select a section:", sections)

        if self.state.selected_section == "Section 1":
            st.write("You selected Section 1")
            # Add code to display Section 1
        elif self.state.selected_section == "Section 2":
            st.write("You selected Section 2")
            # Add code to display Section 2
        elif self.state.selected_section == "Section 3":
            st.write("You selected Section 3")
            # Add code to display Section 3

        self.state.save_state()
