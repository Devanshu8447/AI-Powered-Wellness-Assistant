# AI-Powered Wellness Assistant

## About
The AI-Powered Wellness Assistant is an interactive Python application designed to provide personalized wellness support through AI-driven chat. It helps users by answering wellness-related questions and providing guidance in areas such as general health, diet, and mental well-being, all through an intuitive web interface.

## Features
The assistant includes specialized agents to address multiple wellness domains:

- **General Physician Agent**
  - Offers general medical information and guidance on common health queries.
  
- **Diet Planner Agent**
  - Provides personalized nutrition and diet plans tailored to individual needs.
  
- **Mental Health Agent**
  - Supports mental well-being with advice on stress management, emotional health, and mindfulness.

Additional features include:
- Upload PDFs dynamically to expand the assistant’s knowledge base.
- Manage multiple chat sessions with persistent history.
- Easy-to-use Streamlit web interface for conversation and document uploads.
- Backend powered by advanced language models to generate contextual and helpful responses.

## Installation
1. Clone the repository:
git clone https://github.com/Devanshu8447/AI-Powered-Wellness-Assistant.git
cd AI-Powered-Wellness-Assistant

2. (Recommended) Create and activate a Python virtual environment:
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate

3. Install the project dependencies:
pip install -r requirements.txt

4. Add your Groq API key in a `.env` file:
GROQAPIKEY=your_groq_api_key_here

## Usage
Start the Streamlit app by running:
streamlit run frontend.py

- Upload wellness-related PDFs in the sidebar to add more content for the assistant.
- Use the chat interface to ask questions and receive advice from the different wellness agents.
- Switch between multiple chat threads to maintain separate conversations.

## Code Structure
- `frontend.py`: Handles the Streamlit user interface, chatbot interaction, and file uploads.
- `backend.py`: Implements document loading, language model querying, chat session management, and wellness agents.
- `requirements.txt`: Lists all Python package dependencies.

## License
This project is licensed under the MIT License.

## Contributing
Contributions, issues, and feature requests are welcome! Please fork the repository and submit pull requests.

---

This assistant combines AI conversational techniques to provide accessible and personalized wellness advice covering physical health, diet, and mental well-being.
