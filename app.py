from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
from markupsafe import Markup
import google.generativeai as genai
import re
import random
import os
from dotenv import load_dotenv
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure server-side session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)
# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("API_KEY")

# Configure the Generative AI model with the API key
genai.configure(api_key=api_key)


generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 1000,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

system_instruction = """You are an expert named Recom-AI, specialized in recommending movies, web series, books, restaurants, and online courses.

1. Identify what kind of recommendation the user wants, and just give the response in this manner,
 unless the user does not specify any number, give at least 3 different recommendations:
Things to include in your responses for each category:

i. Movies:
   - Title, synopsis, genres, rating, top 3 lead actors/actresses, director.
ii. Books:
   - Title, synopsis, genres, author, rating.
iii. Web Series:
   - Title, synopsis, genres, top 3 lead actors/actresses, platform.
iv. Online Courses:
   - Course name, instructor, platform, rating.
v. Restaurants:
   - Name, area, rating, cuisine, average price for two.
2. If the user asks about specific preferences or aspects of a recommendation, engage with them to better understand their needs.
3. If the user asks something unrelated, politely inform them that you can't answer that and offer assistance with recommendations.

To maintain context during the conversation:
- Remember the user's previous query and use it to guide subsequent responses.
- Avoid asking repetitive or unnecessary questions, unless clarification is genuinely needed.
- If the user provides additional information in response to a question, incorporate it into the ongoing conversation without restarting the dialogue.

"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    system_instruction=system_instruction,
    safety_settings=safety_settings
)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    
    # Retrieve previous context from session
    conversation_history = session.get('conversation_history', [])
    
    # Append the new user input to the conversation history
    conversation_history.append("User: " + user_input)
    
    # Create the prompt with conversation history
    prompt = "\n".join(conversation_history)
    
    # Generate response
    response = model.generate_content([prompt])
    formatted_response = format_response(response.text)
    
    # Append the bot response to the conversation history
    conversation_history.append("Recom-AI: " + response.text)
    
    # Update the session with the new conversation history
    session['conversation_history'] = conversation_history

    return jsonify({'response': Markup(formatted_response)})

def format_response(text):
    # Replace the specific headings with bold tags and add line breaks for readability
    replacements = {
        "\n": "<br>",
        "Synopsis:": "<b>Synopsis:</b>",
        "Genres:": "<b>Genres:</b>",
        "Rating:": "<b>Rating:</b>",
        "Top 3 Lead Actors/Actresses:": "<b>Top 3 Lead Actors/Actresses:</b>",
        "Director:": "<b>Director:</b>",
        "Instructor:": "<b>Instructor:</b>",
        "Platform:": "<b>Platform:</b>",
        "Area:": "<b>Area:</b>",
        "Cuisine:": "<b>Cuisine:</b>",
        "Average price for two:": "<b>Average price for two:</b>",
        "Average Price for Two": "<b>Average Price for Two</b>",
        "Author:": "<b>Author:</b>"
    }

    for key, value in replacements.items():
        text = text.replace(key, value)
    
    # Convert Markdown bold to HTML bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    return text


if __name__ == '__main__':
    app.run(debug=True)
