# Asha AI Chatbot

Asha AI is a virtual assistant for women's career development and empowerment. It provides:
- Job, event, and mentorship program search
- Bias detection and mitigation in chat
- Positive reinforcement detection
- Powered by Groq Llama 3.3 (via Groq API)
- Modern, animated UI with Streamlit

## Features
- **Conversational AI**: Uses Llama 3.3 via Groq API for natural, contextual responses
- **Bias Detection**: Identifies and suggests mitigation for gender bias in chat
- **Career Resources**: Search jobs, events, and mentorship programs from sample data
- **Animated UI**: Modern, responsive, and visually engaging interface

## Setup

### 1. Clone the repository
```bash
git clone <repo-url>
cd asha-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root directory and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Prepare sample data
Sample CSV files for jobs, events, and mentorship programs are in the `data/` directory. You can edit or expand these as needed.

### 5. Run the app
```bash
streamlit run app.py
```

## Usage
- Type your questions or requests in the chat input.
- The assistant will respond, detect bias, and show relevant career resources.
- Bias and positive reinforcement are visually highlighted.

## Technologies Used
- [Streamlit](https://streamlit.io/)
- [Groq API](https://console.groq.com/) (Llama 3.3)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/python/)

## Customization
- Update the data in `data/` for your own jobs, events, or mentorship programs.
- Tweak the UI and CSS in `app.py` for your branding.
