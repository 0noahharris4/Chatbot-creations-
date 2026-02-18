import streamlit as st
from openai import OpenAI

# Property context for AI responses
PROPERTY_CONTEXT = """
You are Dave, an expert property assistant for Clear Water Apartments, a luxury apartment building in Malibu California. You have extensive knowledge of the property, units available, leasing information, nearby amenities, and the local area. Your role is to provide accurate and helpful information to prospective and current residents about the property, leasing processes, amenities, and local attractions.

Current Property Information:
- Available Units: 
  * Unit 101: 1 bed, 1 bath - $2,500/month - Available for move-in March 1, 2026
  * Unit 201: 2 bed, 2 bath - $3,800/month - Available for move-in February 15, 2026
  * Unit 202: 2 bed, 2 bath - $3,800/month - Available for move-in April 1, 2026
  * Unit 301: 1 bed, 1 bath - $2,500/month - Available for move-in February 20, 2026
  * Unit 302: 3 bed, 2 bath - $5,200/month - Available for move-in May 1, 2026

- Pricing Information:
  * 1 Bedroom: Starting at $2,500/month
  * 2 Bedroom: $3,800/month
  * 3 Bedroom: Starting at $5,200/month
  * All prices include utilities (water, trash, high-speed internet)
  * Prices are subject to lease terms (discounts available for longer commitments)

- Building Amenities: Fitness center, movie theater, tennis courts, swimming pool, rooftop lounge, 24/7 concierge, and underground parking.
- Lease Terms Available: Month-to-month, 3 Months, 6 Months, and 12 months. Typically, 30-day notice for move-out
- Move in costs: Security deposit equal to $100 (returned after move-out if no damage) and a $25 application fee.
- Pet Policy: Up to 2 pets allowed with $300 pet deposit per pet

When answering questions about availability, move-in dates, or other property details, be professional, friendly, and accurate. 
Always encourage them to contact the leasing office for more information or to schedule a tour.
"""

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    return OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

#Defining function to retreive the proper response to the end users question
def get_bot_response(user_input):
    user_input_lower = user_input.lower()
    
    #Multi-word phrase matching 
    
    # Late payment questions
    if ("late" in user_input_lower and "payment" in user_input_lower) or "late fee" in user_input_lower:
        return "Rent is due on the 1st of each month. A late fee of $50 will be applied if payment is received after the 5th. Please check your lease for specific details."
    
    # Portal access questions
    if ("access" in user_input_lower and "portal" in user_input_lower) or ("how" in user_input_lower and "portal" in user_input_lower):
        return "The payment portal can be accessed through our website or the resident app. Use your email and password to log in. If you have trouble, contact the office for assistance."
    
    # Rent due date questions
    if ("when" in user_input_lower and "rent" in user_input_lower and "due" in user_input_lower) or ("rent due" in user_input_lower):
        return "Rent is due on the 1st of each month. A late fee of $50 will be applied if payment is received after the 5th. Please check your lease for specific details."
    
    # Package delivery questions
    if ("package" in user_input_lower or "packages" in user_input_lower) and ("deliver" in user_input_lower or "delivery" in user_input_lower or "delivered" in user_input_lower):
        return "Packages are generally delivered to your front door, placed inside of your mailbox, or delivered to the package room. You'll receive a notification via the resident mobile app when your package is ready for pickup."
    
    # Office hours questions
    if "office hours" in user_input_lower or ("when" in user_input_lower and "office" in user_input_lower) or ("hours" in user_input_lower and "open" in user_input_lower):
        return "Our leasing office is open Monday–Friday from 9am–5pm and Saturday 10am–4pm. We are closed on Sundays and major holidays."
    
    # Maintenance/repair questions
    if ("maintenance" in user_input_lower or "repair" in user_input_lower or "broken" in user_input_lower) and ("submit" in user_input_lower or "request" in user_input_lower or "how" in user_input_lower):
        return "To submit a maintenance request, log into the resident portal and select 'Maintenance'. For emergencies like leaks or no heat, call our 24/7 line immediately."
    
    # Parking questions
    if ("parking" in user_input_lower or "garage" in user_input_lower or "spot" in user_input_lower) or ("permit" in user_input_lower and "parking" in user_input_lower):
        return "Parking permits are issued through the leasing office. Each resident will be given an assigned parking spot. Guest parking is limited."
    
    # Move-out policy questions
    if ("move" in user_input_lower and "out" in user_input_lower) or "move-out" in user_input_lower or ("notice" in user_input_lower and "move" in user_input_lower):
        return "Our move-out policy requires a 30-day written notice. Please refer to your lease agreement for specific details and any associated fees."
    
    # Contact/communication questions
    if ("contact" in user_input_lower and ("office" in user_input_lower or "leasing" in user_input_lower)) or ("how" in user_input_lower and "reach" in user_input_lower) or ("email" in user_input_lower and "phone" in user_input_lower):
        return "You can contact the leasing office by calling (555) 123-4567 or emailing leasing@ourproperty.com. We're here to help with any questions or concerns you may have."
    
    # Utilities questions
    if ("utilities" in user_input_lower) or ("water" in user_input_lower or "electric" in user_input_lower or "gas" in user_input_lower or "wifi" in user_input_lower or "internet" in user_input_lower) and ("included" in user_input_lower or "bill" in user_input_lower or "pay" in user_input_lower):
        return "Utilities are set up directly with providers. Water and trash are billed independently through the property. Check your lease for additional details."
    
    # Thank you/gratitude
    if "thank" in user_input_lower or "thanks" in user_input_lower or "thx" in user_input_lower:
        return "You're welcome! Is there anything else that I can assist you with today?"
    
    # Fallback: Use OpenAI for questions not in hard-coded rules
    try:
        with st.spinner():
            client = get_openai_client()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": PROPERTY_CONTEXT},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=150
            )
        return response.choices[0].message.content
    except Exception as e:
        return "I'm not sure I understand your inquiry. Could you please rephrase that, or contact our leasing office at (555) 123-4567?"

# ⚙️ Page config
st.set_page_config(page_title="Clear Water Appartments Digital Assistant", page_icon="🏠")

#Implementing custom background for luxury apartments theme
st.markdown("""
<style>
[data-testid="stAppViewContainer"] > div:first-child {
    background-image: linear-gradient(rgba(20,20,30,0.6), rgba(20,20,30,0.6)),
                      url("https://images.pexels.com/photos/1457842/pexels-photo-1457842.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=1080");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
body {
    background-color: #0a0a14;
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
    margin: 10px 0;
    width: 100%;
    box-sizing: border-box;
}
.user-bubble {
    background-color: #d1e7dd;
    padding: 10px;
    border-radius: 10px;
    margin: 10px 0;
    width: 100%;
    box-sizing: border-box;
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
st.markdown('<div class="chat-title">💬 Chat with Dave – Your 24/7 Property Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-prompt">How can I help you today?</div>', unsafe_allow_html=True)

#chat history with end user 
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#Input handler
def handle_input():
    user_input = st.session_state.get("user_input_value", "")
    if user_input:
        response = get_bot_response(user_input)
        st.session_state.chat_history.append(("User", user_input))
        st.session_state.chat_history.append(("Dave", response))
        st.session_state["user_input_value"] = ""  # Clear input after handling

#Chat history - display only the most recent message exchange
if st.session_state.chat_history:
    # Show only the last 2 messages (latest user message and bot response)
    for sender, message in st.session_state.chat_history[-2:]:
        bubble_class = "user-bubble" if sender == "User" else "chat-bubble"
        st.markdown(f'<div class="{bubble_class}"><strong>{sender}:</strong> {message}</div>', unsafe_allow_html=True)

#Single input field
st.text_input(
    label="",
    key="user_input_value",
    on_change=handle_input,
    placeholder="Type your message here...",
    label_visibility="hidden"
)
