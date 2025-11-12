import streamlit as st

# 🎯 Rule-based responses to end users questions 
rules = {
    ("return", "refund", "doesn't fit", "too small"): "Sure! To start a return or refund, please visit your order history and select the item.",
    ("shipping", "delivery", "did not receive"): "Standard shipping takes 3–5 business days. You’ll receive tracking info once it ships.",
    ("cancel",): "To cancel an order, go to your orders page and click 'Cancel' next to the item.",
    ("hours", "open", "representative"): "Our support team is available 24/7 via chat and email!",
    ("agent", "human"): "I’ll connect you with a human agent. Please hold on a moment...",
    ("hello", "hi", "hey"): "Hi there! 👋 How can I assist you today?",
    ("thank", "thank you"): "You're very welcome! Let me know if there's anything else I can help with."
}
#Defining function to retreive the proper response to the end users question/inquiry
def get_bot_response(user_input):
    user_input = user_input.lower()
    for keywords, reply in rules.items():
        if any(keyword in user_input for keyword in keywords):
            return reply
    return "I'm not sure I understand. Could you rephrase that or ask about returns, shipping, or cancellations?"

# ⚙️ Page config
st.set_page_config(page_title="Botly - Ecommerce Chatbot", page_icon="🛍️")

#Implementing custom background for shopping theme
st.markdown("""
<style>
[data-testid="stAppViewContainer"] > div:first-child {
    background-image: linear-gradient(rgba(44,44,44,0.7), rgba(44,44,44,0.7)),
                      url("https://images.pexels.com/photos/19294576/pexels-photo-19294576.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=1080");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
body {
    background-color: #2c2c2c;
}
</style>
""", unsafe_allow_html=True)

#Implementing custom background for shopping theme
st.markdown("""
<style>
.chat-container {
    background-color: rgba(255, 255, 255, 0.85);
    padding: 20px;
    border-radius: 10px;
    max-width: 700px;
    margin: 30px auto;
}
.chat-bubble {
    background-color: #f1f1f1;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}
.user-bubble {
    background-color: #d1e7dd;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    text-align: right;
}
.chat-title {
    font-size: 24px;
    font-weight: bold;
    color: white;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 5px;
}
.custom-prompt {
    font-size: 18px;
    margin-bottom: 10px;
    color: white;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

#Title and prompt
st.markdown('<div class="chat-title">💬 Chat with Botly – Your 24/7 Ecommerce Helper</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-prompt">How can I help you today?</div>', unsafe_allow_html=True)

#Clear chat button
if st.button("🖊️ Clear Chat"):
    st.session_state.chat_history = []

#chat history with end user 
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#Input handler
def handle_input():
    user_input = st.session_state.get("user_input_value", "")
    if user_input:
        response = get_bot_response(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Botly", response))
        st.session_state["user_input_value"] = ""  # Clear input after handling

#Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

#Chat history
for sender, message in st.session_state.chat_history:
    bubble_class = "user-bubble" if sender == "You" else "chat-bubble"
    st.markdown(f'<div class="{bubble_class}"><strong>{sender}:</strong> {message}</div>', unsafe_allow_html=True)

#Single input field — no extra box above or below
st.text_input(
    label="",
    key="user_input_value",
    on_change=handle_input,
    placeholder="Type your message here...",
    label_visibility="hidden"
)

st.markdown('</div>', unsafe_allow_html=True)