import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as palm
from langdetect import detect
from googletrans import Translator, LANGUAGES

load_dotenv()
Api_key = os.getenv("API_KEY")

palm.configure(api_key=Api_key)
translator = Translator()

i = 0
model_list = palm.list_models()
for model in model_list:
    if i == 1:
        model_name = model.name
        break
    i += 1

def generate_questions(model_name, text):
    response = palm.generate_text(
        model=model_name,
        prompt=f"Generate generate follow-up questions which are intriguing and thought-provoking from the provided context text:\n\n{text}\n\nQuestions:",
        max_output_tokens=150
    )

    questions = response.result.strip() if response.result else "No questions generated"

    return questions

def get_user_text():
    return st.text_area("Enter the text you want questions generated from:")

def process_and_generate_questions(user_text, model_name):
    try:
        detected_language = detect(user_text)

        if detected_language != 'en':
            translated_text = translator.translate(user_text, src=detected_language, dest='en').text
        else:
            translated_text = user_text

        questions = generate_questions(model_name, translated_text)

        if detected_language != 'en':
            questions = translator.translate(questions, src='en', dest=detected_language).text

        return questions
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def main():
    st.title("Inquisitive")

    user_text = get_user_text()

    if st.button("Generate Questions"):
        questions = process_and_generate_questions(user_text, model_name)
        if questions:
            st.subheader("Generated Questions:")
            st.write(questions)
    if not user_text:
        st.warning("Please enter some text.")
        return
if __name__ == "__main__":
    main()