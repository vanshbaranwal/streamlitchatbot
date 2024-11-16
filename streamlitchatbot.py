import streamlit as st
import random
from datetime import datetime
import time

# Initialize session state for user name, messages, and acknowledgment flag
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "name_entered" not in st.session_state:
    st.session_state.name_entered = False
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
if "conversation_ended" not in st.session_state:
    st.session_state.conversation_ended = False  # To track if the conversation ended

# Fun greeting messages
greetings = [
    "Hello! What's your name today?",
    "Hey! Let’s start by getting to know you. What’s your name?",
    "Greetings! Tell me your name, and we'll begin our journey."
]

# Motivational quotes or jokes
quotes = [
    "Keep smiling! 😄",
    "What do you call a bot with a sense of humor? A chatty-bot! 😂",
    "Life is better with friends—and bots! 🚀"
]

# Page 1: Name Input
if st.session_state.user_name is None or not st.session_state.chat_started:
    # Fun bot introduction
    st.title("Welcome to Chat BOT! 💡")
    st.subheader("Hi there! I'm your chatbot 🤖. Let's get started!")
    
    # Randomized greeting or time-based greeting
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good Morning! Tell me your name."
    elif current_hour < 18:
        greeting = "Good Afternoon! Tell me your name."
    else:
        greeting = "Good Evening! Ready to chat?"
    
    st.header(greeting)
    
    # Add a horizontal divider
    st.divider()
    
    # Input field for user name
    user_name = st.text_input("Your Name", key="name_input", placeholder="Type your name here...")

    # Enter button to confirm name
    if st.button("Enter"):
        if user_name.strip():
            st.session_state.user_name = user_name.strip()
            st.session_state.name_entered = True
        else:
            st.error("Name cannot be empty. Please enter your name.")
    
    # Display a motivational quote or joke
    st.write(random.choice(quotes))
    
    # Display a message after the name is entered
    if st.session_state.name_entered:
        st.write("<h3 style='color: yellow;'>✨ Welcome, {}</h3>".format(st.session_state.user_name), unsafe_allow_html=True)
        st.success("Press the Start Chat button to continue to the chatbot.")

    # Start Chat button to proceed
    if st.button("Start Chatting"):
        if st.session_state.name_entered:
            st.session_state.chat_started = True  # Flag to indicate chat has started

            # Simulate progress bar effect
            with st.spinner("Loading your chatbot..."):
                progress = st.progress(0)  # Initialize the progress bar
                for i in range(101):  # Increment from 0 to 100
                    time.sleep(0.01)  # Adjust for speed
                    progress.progress(i)
                st.success("Chatbot loaded! 🚀")
        else:
            st.error("Please enter your name and press Enter first.")

# Page 2: Chatbot (Only shown if conversation hasn't ended)
elif st.session_state.chat_started and not st.session_state.conversation_ended:
    st.title(f"Welcome, {st.session_state.user_name}! 🤖")
    st.header("Chat BOT: Let's Chat... 🚀")
    st.divider()

    # Icons for the user and bot
    bot_icon = "🤖"
    user_icon = "👨‍💻"

    # Display previous messages in the chat
    for message in st.session_state.messages:
        role = user_icon if message["role"] == "user" else bot_icon
        st.write(f"{role}: {message['content']}")

    # Input field for user messages
    user_input = st.chat_input("Type your message here...")

    # Process user input if it exists
    if user_input:
        # Command to delete chat history
        if user_input.lower() == "delete history":
            st.session_state.messages.clear()
            st.write(f"{bot_icon} : Chat history has been deleted.")
        
        # Command to view chat history
        elif user_input.lower() == "history":
            if st.session_state.messages:
                # Create a structured format for chat history
                st.divider()
                st.write(f"{bot_icon} : Here is your chat history:")
                st.divider()
                for msg in st.session_state.messages:
                    role = user_icon if msg["role"] == "user" else bot_icon
                    st.markdown(f"**{role}**: {msg['content']}")
                st.divider()
            else:
                bot_response = "No chat history available."
                st.write(f"{bot_icon} : {bot_response}")
                st.divider()
                
                # Append bot's response to the session state
                st.session_state.messages.append({"role": "bot", "content": bot_response})

        # Command to exit the chat
        elif user_input.lower() == "exit":
            st.write(f"{bot_icon} : Bye, {st.session_state.user_name}!")
            st.write(f"{bot_icon} : Enter 'bye' to exit.")
            
            # Set the flag for conversation ended
            st.session_state.conversation_ended = True

            # Clear session state to reset for future conversations
            # st.session_state.chat_started = False
            st.session_state.messages.clear()

        # Regular message processing (echo response)
        else:
            # Append user message to session state
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.write(f"{user_icon} : {user_input}")
            
            # Generate bot response and append to session state
            bot_response = f"You said: {user_input}"
            st.session_state.messages.append({"role": "bot", "content": bot_response})
            st.write(f"{bot_icon} : {bot_response}")

# Page 3: Conversation Ended Page (Only shown if conversation has ended)
elif st.session_state.conversation_ended:
    st.title("Conversation Ended!")
    st.markdown(f"**It was great talking to you, {st.session_state.user_name}!** 😊")
    st.write("Thanks for chatting with me! Hope to see you again soon. 👋")
