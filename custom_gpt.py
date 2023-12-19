import streamlit as st
import openai
import os
import pickle

# For this example, let's just use the conversation model
openai.api_key = "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"

# Check if the pickle file for saving conversations exists
if os.path.isfile("conversations.pkl"):
    # If exists, then load the previous conversations
    with open("conversations.pkl", "rb") as f:
        conversations = pickle.load(f)
else:
    # If not exist, then start a new list for saving conversations
    conversations = []
    
if st.button("Clear Conversation"):
    # Clear the conversation list and delete the pickle file
    conversations = []
    os.remove("conversations.pkl")
    st.info("Conversation cleared!")


# Display previous conversations
st.title("Previous Conversations")
for conversation in conversations:
    st.markdown(f"**User:** {conversation['user']}")
    st.markdown(f"**Assistant:** {conversation['assistant']}")

# Input field
user_input = st.text_input("Enter your message")

# Submit button
if st.button("Submit"):
    # Send the user's message to OpenAI API
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{user_input}"},
        ],
    )

    assistant_response = response.choices[0].message.content

    # Save the conversation
    conversations.append({"user": user_input, "assistant": assistant_response})
    with open("conversations.pkl", "wb") as f:
        pickle.dump(conversations, f)

    # Display the response
    st.markdown(f"**Assistant:** {assistant_response}")