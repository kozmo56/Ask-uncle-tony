import streamlit as st
from openai import OpenAI

# The secret key connects your app to OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Ask Uncle Tony 🤌")
st.write("Tell Uncle Tony your problem, but keep it quick. He's tabbing soon.")

# Paste the System Prompt we drafted earlier right here between the triple quotes
SYSTEM_PROMPT = """
You are "Uncle Tony." You are not an AI assistant; you are a wise-cracking, street-smart, slightly arrogant, but ultimately loving uncle.
[PASTE THE REST OF THE PROMPT FROM OUR PREVIOUS CHAT HERE]
"""

# Initialize the chat history
if "messages" not in st.session_state:
    # Give the AI its instructions
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    # Give Uncle Tony an opening greeting
    st.session_state.messages.append({"role": "assistant", "content": "What's the situation? Don't try to make me crazy."})

# Display previous messages on the screen
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Wait for the user to type a problem
if prompt := st.chat_input("What's the situation?"):
    # Show the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Get Uncle Tony's response from OpenAI
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo", # This is the fast, cheap model. 
            messages=st.session_state.messages,
            stream=True
        )
        response = st.write_stream(stream)
        
    # Save the response to the chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
