# Import libraries
import google.generativeai as genai

genai.configure(api_key="AIzaSyCZQHx_6V4tNhtzDCKEdj6_4WZQchfrwA0")  # Replace with your API key

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

1. identify what kind of recommendation the user wants, and just give the response in this manner,
 unless user does not specify any number, give atleast 3 different recommendations:
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

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

def get_response(user_input):
    if user_input.lower() == "exit":
        return "Goodbye! Have a great day!"
    prompt_parts = ["\n" + user_input + "\n"]
    response = model.generate_content(prompt_parts)
    return response.text

if __name__ == "__main__":
    print("Hello! I'm rec-ai, your go-to expert for all things entertainment and learning. "
          "Feel free to ask me about movies, web series, books, restaurants, or online courses.")
    get_response()  # This line is removed as we don't call this function directly
