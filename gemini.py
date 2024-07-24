# Load environment variables
import os
import textwrap

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# configure gemini
gemini_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
wrapper = textwrap.TextWrapper(width=50)


def get_response(prompt):
    response = model.generate_content(f'''
    You are a knowledgeable agricultural expert chatbot designed to assist farmers with their queries.
    Your target audience is small-scale farmers in rural areas with limited agricultural knowledge.
    Respond in a friendly, informative, and helpful manner, using simple language.
    Generate responses in less than 400 character count.
    Here is their question, "{prompt}".''')
    return wrapper.fill(response.text.replace('*', ''))


print(get_response('What are the best crops to grow in a dry climate in Northern Nigeria?'))
