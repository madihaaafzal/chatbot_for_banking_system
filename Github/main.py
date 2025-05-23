import streamlit as st
import os
import pandas as pd
import hashlib
from dotenv import load_dotenv
from openai import OpenAI 


# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set page configuration
st.set_page_config(page_title="AI Banking Assistant", layout="wide")

# Custom CSS for Background and Styling
st.markdown(r"""
    <style>
        /* Background and layout styling */
        .hero-section {
            background-image: url('https://images.pexels.com/photos/4968639/pexels-photo-4968639.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');
            background-size: cover;
            background-position: center;
            padding: 60px 30px;
            border-radius: 12px;
            color: #f8f9fa;
            text-align: center;
        }

        .chat-box {
            background: rgba(30, 30, 30, 0.9);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }

        .section-box {
            background: rgba(40, 40, 40, 0.95);
            padding: 15px 20px;
            margin-top: 20px;
            border-radius: 8px;
            box-shadow: 0px 1px 6px rgba(255,255,255,0.1);
            color: #f1f1f1;
        }

        input[type="text"], input[type="password"], textarea {
            color: #ffffff !important;
            background-color: #333 !important;
            border: 1px solid #555 !important;
        }

        ::placeholder {
            color: #cccccc !important;
        }
    </style>
""", unsafe_allow_html=True)


# ------------------ User Auth Logic ------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists("users.csv"):
        return pd.read_csv("users.csv")
    else:
        return pd.DataFrame(columns=["username", "password"])

def save_user(username, password):
    users_df = load_users()
    username = username.lower()
    if username in users_df["username"].values:
        return False
    hashed = hash_password(password)
    new_user = pd.DataFrame({"username": [username], "password": [hashed]})
    new_user.to_csv("users.csv", mode='a', header=not os.path.exists("users.csv"), index=False)
    return True

def authenticate(username, password):
    users_df = load_users()
    username = username.lower()
    hashed_pw = hash_password(password)
    return any((users_df["username"] == username) & (users_df["password"] == hashed_pw))

# ------------------ Session State Setup ------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "login"

# ------------------ Login/Signup UI ------------------
if not st.session_state.authenticated:
    if st.session_state.page == "login":
        st.title("🔒 Login to AI Banking Assistant")
        username = st.text_input("Username").strip()
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username and password and authenticate(username, password):
                st.success("✅ Login successful!")
                st.session_state.authenticated = True
            else:
                st.error("❌ Invalid username or password.")
        if st.button("Go to Sign Up"):
            st.session_state.page = "signup"
        st.stop()

    elif st.session_state.page == "signup":
        st.title("📝 Create New Account")
        new_username = st.text_input("Choose a Username").strip()
        new_password = st.text_input("Choose a Password", type="password")
        if st.button("Sign Up"):
            if new_username and new_password:
                if save_user(new_username, new_password):
                    st.success("🎉 Account created! Please log in.")
                    st.session_state.page = "login"
                else:
                    st.warning("⚠️ Username already exists.")
            else:
                st.warning("Please enter both username and password.")
        if st.button("Back to Login"):
            st.session_state.page = "login"
        st.stop()

# ------------------ Hero Section ------------------
st.markdown("""
<div class='hero-section'>
    <h1 style='color: #fafafa;'>🏦 AI Based Banking Bot System</h1>
    <p>Get expert answers to your banking-related queries in Pakistan</p>
</div>
""", unsafe_allow_html=True)

# ------------------ Chat Section ------------------
st.markdown("""
<div class='chat-box'>
    <h3 style="color: white; background-color: #1a1a1a; padding: 10px; border-radius: 6px;">
        🤖 Ask Your Banking Assistant
    </h3>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.text_input("Type your banking question here:")

if user_query:
    with st.spinner("Thinking..."):
        try:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": (
                        "You are a professional banking assistant for Pakistan. Only answer questions "
                        "related to Pakistani banking. For unrelated questions, reply: "
                        "'I'm your banking assistant and can only help with banking-related queries in Pakistan.'"
                    )},
                    *st.session_state.chat_history
                ]
            )
            reply = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.success(reply)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)


# ------------------ Banking Tip ------------------
import random  # Add this at the top if not already imported

banking_tips = [
    "Always compare annual profit rates and service fees before opening a savings account in Pakistan.",
    "Use mobile banking apps to track your expenses and set savings goals.",
    "Avoid withdrawing cash from ATMs that charge extra fees.",
    "Enable SMS alerts to monitor transactions and detect fraud early.",
    "Never share your ATM PIN or online banking credentials with anyone.",
    "Use biometric authentication for added security in mobile banking apps.",
    "Keep your contact details updated with your bank to receive timely alerts.",
    "Prefer banks with a wide ATM network for easier cash access without charges.",
    "Set up auto-debit for monthly bills to avoid late payment penalties.",
    "Monitor your credit score regularly to stay eligible for loans.",
    "Always read the terms and conditions before signing up for credit cards.",
    "Consider Islamic banking if you prefer interest-free financial products.",
    "Use internet banking to manage accounts, pay bills, and transfer funds safely.",
    "Ask about hidden charges when opening fixed deposit accounts.",
    "Avoid clicking on unknown links claiming to be from your bank.",
    "Check for annual charges on debit/credit cards before applying.",
    "Use two-factor authentication on your online banking accounts.",
    "Divide savings across multiple banks for added financial security.",
    "Don't ignore bank SMS alerts—they may warn of unauthorized activity.",
    "Set monthly budgets and stick to them to improve financial discipline."
]

selected_tip = random.choice(banking_tips)

st.markdown(f"""
<div class='section-box'>
    <h4>📌 Smart Banking Tip of the Day</h4>
    <p>{selected_tip}</p>
</div>
""", unsafe_allow_html=True)


# ------------------ Bank Locator ------------------
st.markdown("""
<div class='section-box'>
    <h4>📍 Find a Nearby Bank</h4>
    <p>Click below to search banks near your location on Google Maps:</p>
    <a href='https://www.google.com/maps/search/banks+near+me/' target='_blank' style='color:#4fc3f7; text-decoration: none;'>🔗 Locate Banks</a>
</div>
""", unsafe_allow_html=True)

# ------------------ Feedback Form ------------------
st.markdown("""
<div class='section-box'>
    <h4>💬 We Value Your Feedback</h4>
    <p style='font-size: 15px;'>Help us improve! Share your thoughts or suggestions below.</p>
</div>
""", unsafe_allow_html=True)

with st.form("feedback_form"):
    name = st.text_input("Your Name (optional)")
    feedback = st.text_area("Your Feedback", placeholder="Type your feedback here...")
    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        if feedback.strip() == "":
            st.warning("⚠️ Please write some feedback before submitting.")
        else:
            feedback_df = pd.DataFrame({
                "Name": [name],
                "Feedback": [feedback],
                "Source": ["Banking Assistant App"]
            })

            if os.path.exists("user_feedback.csv"):
                feedback_df.to_csv("user_feedback.csv", mode='a', header=False, index=False)
            else:
                feedback_df.to_csv("user_feedback.csv", index=False)

            st.success("🙏 Thank you for your feedback!")

# ------------------ Footer ------------------
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px;'>© 2025 AI Banking Assistant | Developed by Madiha Afzal Student of BSCS Islamia University Of Bahawalpur</p>", unsafe_allow_html=True)



