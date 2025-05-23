🏦 AI Banking Assistant
An intelligent Streamlit web application that acts as a professional banking assistant for users in Pakistan. It leverages OpenAI’s GPT model to respond to banking-related queries and features user authentication, banking tips, and feedback collection.

🚀 Features
🤖 AI-Powered Chatbot – Ask questions about Pakistani banking, and get smart, context-aware responses.

🔐 User Authentication – Secure signup and login functionality with password hashing.

💡 Banking Tips – Get a daily smart tip to improve your financial literacy.

📍 Bank Locator – Quick access to Google Maps to find nearby banks.

💬 Feedback Form – Users can share feedback to improve the application.

🛠️ Tech Stack
Python

Streamlit – UI framework

OpenAI API – Chatbot intelligence

dotenv – Environment variable management

Pandas – Data management (for users and feedback)

📁 Project Structure
bash
Copy
Edit
📦 AI-Banking-Assistant/
├── main.py                 # Main Streamlit application
├── .env                    # Environment file for API key
├── requirements.txt        # Python dependencies
├── user_feedback.csv       # Stores submitted feedback
├── users.csv               # Stores registered user credentials (hashed)
⚙️ Setup Instructions
Clone the repository

bash
Copy
Edit
git clone https://github.com/yourusername/ai-banking-assistant.git
cd ai-banking-assistant
Create a virtual environment (optional but recommended)

bash
Copy
Edit
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set up .env file

Create a file named .env in the root directory and add your OpenAI API key:

ini
Copy
Edit
OPENAI_API_KEY=your-openai-api-key-here
🚨 Do not share this file or commit it to version control.

▶️ Run the Application
bash
Copy
Edit
streamlit run main.py
The app will launch in your default web browser.

👥 User Guide
New users can create an account from the signup page.

Returning users must log in to access the chatbot.

Ask only banking-related questions specific to Pakistan.

Submit feedback using the form at the bottom of the app.

📌 Example Prompts
"How can I open a savings account in HBL?"

"What are the current markup rates for car financing in Pakistan?"

"What is the minimum balance for a Meezan Bank account?"

📃 License
This project is for educational and non-commercial purposes. Feel free to build upon it with proper attribution.

👩‍💻 Author
Developed by Madiha Afzal, BSCS Student at Islamia University of Bahawalpur.
