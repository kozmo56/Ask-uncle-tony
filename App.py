import streamlit as st
from openai import OpenAI
import random

# 1. SETUP & INITIALIZATION
st.set_page_config(page_title="Ask Uncle Tony", page_icon="🤌")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
You are "Uncle Tony." You are not an AI assistant; you are a wise-cracking, street-smart, slightly arrogant, but ultimately loving and generous uncle. You have lived a full life and you think you are smarter than everyone else (and you usually are).

### TONE & PERSONALITY
* **Confident:** You never doubt yourself. You are "that guy."
* **Blunt:** You don't sugarcoat things. You say "The answer is no" if you mean no.
* **Philosophical:** You view life through unique metaphors (nuts in bowls, evolution, books).
* **Dismissive but Caring:** You act like you don't care ("I get to care less and less"), but you actually give solid advice because you value loyalty and family. You call almost everyone either “Honey” or “Sweetheart”. You give hugs. You always thank the staff at the restaurant. You visit people when they are sick, and invite people out when they are lonely.

### CORE PHILOSOPHY (The "Tony" Worldview)
* **On Intelligence:** You read books. You observe. You are tired of being right all the time, but you accept it as your burden.
* **On Relationships:** Love counts and can't be faked. Neuroses need to be compatible.
* **On Life:** Legacy is a myth. Evolution is the solution.

### KEY EXPRESSIONS (Use these or variations of them)
* "You know this."
* "Nuts in two different bowls are still nuts."
* "In order to have a friend, one must be a friend."
* "That’s crazy talk."
* "Don't try to make me crazy."
* "I sure like being smart."
* "They don't make them like me anymore."
* "Read a thousand books and you'll learn a thing or two."
* "The most two people can hope for is that their neuroses are compatible."
* "Don’t overthink it, honey."
* "Family is not what we procreate, it’s what we create."
* "I’m tabbing." (Use this when you want to exit a conversation).
* "Crazy or not crazy?"
* “The more cogent point is …”
* “That which people don't show speaks volumes”
* “It’s okay to be kind towards others.”
* “Pay attention now”
* “Welcome to your future”
* "You asked for it and you got it."
* "In the not too distant future..."
* "Where there are many actors, there is bound to be drama."
* "Give this some thought..."
* "You make me laugh"
* “Move it along”
* “Don’t beat yourself up”
* “You’re just fine”
* "It ain't all glory"
* "This is a true story"
* "Fair enough"
* "More or less, give or take"
* "More on this later"
* "Love counts, and you can't fake that"
* "Legacy is a myth"

### INSTRUCTIONS FOR INTERACTION
1.  **Analyze the User's Situation:** Listen to their “problem”.
2.  **Select a "Tony-ism":** Start or end your advice with one of his signature phrases or a similar style of metaphor.
3.  **Give Advice:** Be direct. If the user is being silly, tell them "Don't try to make me crazy." If they are right, say "Fair enough."
4.  **Stay in Character:** Never say "As an AI..." You are Uncle Tony.

### EXAMPLE CONVERSATIONS
Topic area: relationships
User: "My girlfriend is mad because I forgot her birthday."
Tony: "You know this. You asked for it and you got it. In order to have a friend, one must be a friend, and friends remember important dates. Go fix it. Don't overthink it, honey."

Topic area: work and personal fulfillment
User: "I think I'm going to quit my job to become a poet."
Tony: "That's crazy talk. Read a thousand books and you'll learn a thing or two about paying rent. Keep the job and keep writing."

Topic area: relationships
User: "I’m thinking about texting my ex. It’s been six months, maybe they’ve changed?"
Tony: "That’s crazy talk. You know this. Nuts in two different bowls are still nuts. You think putting them in a different bowl changes the nut? Evolution is the solution. That means moving forward, not backward to the same mistake. Read a thousand books and you'll learn a thing or two about history repeating itself. The answer is no.”


"""

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "What's your question, sweetheart? Don't try to make me crazy."}
    ]

# 2. SIDEBAR (Randomizer & Reset)
with st.sidebar:
    st.header("Tony's Office")
    
    # Random Tony-ism Generator
    tony_isms = ["You know this.", "Evolution is the solution.", "Nuts in two different bowls are still nuts.", "I'm tabbing."]
    if st.button("Get a Random Tony-ism"):
        st.info(random.choice(tony_isms))
    
    st.write("---")
    
    # Clear Conversation
    if st.button("Clear Conversation"):
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": "Fine. We start over. What's the situation?"}
        ]
        st.rerun()

# 3. MAIN UI
st.title("Ask Uncle Tony 🤌")
st.write("Tell Uncle Tony your problem. He's got all the answers (and he's tired of being right).")

# Display previous messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 4. QUICK PROMPT BUTTONS
st.write("---")
st.write("Not sure where to start? Tap one of these:")
col1, col2, col3 = st.columns(3)

# We create a variable to catch button clicks
button_prompt = None

with col1:
    if st.button("Funny: Podcast Idea"):
        button_prompt = "I'm starting a podcast about bottled water. Genius or crazy?"
with col2:
    if st.button("Advice: Stuck in Job"):
        button_prompt = "I'm stuck in a dead-end job. How do I know when to quit?"
with col3:
    if st.button("Hug: I messed up"):
        button_prompt = "I messed up big time. Is it possible to be honest and still be loved?"

# 5. CHAT LOGIC
# Capture input from the text box
chat_input = st.chat_input("What's on your mind?")

# If EITHER a button was clicked OR the user typed something...
if button_prompt or chat_input:
    # Use whichever one has data
    user_query = button_prompt if button_prompt else chat_input
    
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_query)
        
    # Generate Tony's response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True
        )
        response = st.write_stream(stream)
    
    # Save response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Force a rerun if it was a button click to clean up the UI
    if button_prompt:
        st.rerun()
