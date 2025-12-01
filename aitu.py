import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
from PyPDF2 import PdfReader
import random
from googletrans import Translator  # Import Google Translator

# Configure API
api_key = 'api key'  # Replace with your API key
genai.configure(api_key=api_key)

# Translator instance
translator = Translator()

def get_response(input_text):
    """Gets AI response from Gemini AI."""
    try:
        response = chat.send_message(input_text, stream=True)

        # Ensure the response has completed before accessing the final text
        response.resolve()  # Wait for the response to be fully accumulated

        # Now you can access the final text attribute
        if hasattr(response, 'text'):
            return response.text
        else:
            return "No response from AI"

    except Exception as e:
        st.error(f"Error fetching response: {e}")
        return "Error"

# Function to generate speech audio
def speak(text, lang="en"):
    """Converts text to speech and returns an in-memory file."""
    if text.strip():
        tts = gTTS(text=text, lang=lang)  # Change lang for multilingual support
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        return audio_file
    return None

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    """Extracts text from uploaded PDF file."""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_flashcards(text):
    """Generates Q&A flashcards from the extracted text."""
    flashcards = []

    # Example logic to create simple Q&A pairs (this can be expanded)
    if text:
        questions = ["What is the main concept?", "Explain the key idea in one sentence.",
                     "What is the summary of this section?"]
        for question in questions:
            response = get_response(question + " " + text)

            # Ensure you extract the correct response text from the GenerateContentResponse
            flashcards.append({
                "question": question,
                "answer": response  # Directly assign the response
            })
    return flashcards

# Streamlit setup
st.set_page_config(page_title="AI STUDY ASSISTANT")
st.header("🧠 GENMIND AI")

# Initialize chat session
if 'chat' not in st.session_state:
    model = genai.GenerativeModel("gemini-pro")
    st.session_state['chat'] = model.start_chat(history=[])
chat = st.session_state['chat']

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input Mode Selection
input_mode = st.radio("Choose Input Mode:", ["⌨ Text", "📄 PDF"])

# Language Selection for Speech
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Hindi": "hi",
    "Chinese": "zh",
    "Arabic": "ar",
    "Telugu": "te"  # Added Telugu language
}

language = st.selectbox("Choose Language for Speech:", list(languages.keys()))
selected_language = languages.get(language, "en")

# User Input Section
st.subheader("🔍 Ask a Question")

# Text Input
input_text = ""
if input_mode == "⌨ Text":
    input_text = st.text_input("Type your question:", key="input")

# PDF Upload
pdf_file = None
if input_mode == "📄 PDF":
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Submit Button
submit = st.button("🚀 Submit")

# Handle Submission
if submit:
    flashcards = []
    if input_mode == "⌨ Text" and input_text:
        with st.spinner("⏳ AI is thinking..."):
            response = get_response(input_text)
            st.session_state['chat_history'].append(("You", input_text))

            bot_response = response

            # Translate bot response to selected language
            translated_response = translator.translate(bot_response, dest=selected_language).text

            st.session_state['chat_history'].append(("BOT", translated_response))
            st.write(translated_response)

            # Store last response in session state
            st.session_state['last_response'] = translated_response

            # Generate Flashcards
            flashcards = generate_flashcards(bot_response)

            # Playable Audio Response for translated text
            audio_file = speak(translated_response, lang=selected_language)
            if audio_file:
                st.audio(audio_file, format="audio/mp3")

    # Process PDF File
    elif input_mode == "📄 PDF" and pdf_file:
        with st.spinner("⏳ Extracting text from PDF..."):
            pdf_text = extract_text_from_pdf(pdf_file)
            st.write("📄 Extracted Text from PDF:")
            st.text_area("PDF Text", pdf_text, height=200)

            # Generate Flashcards based on PDF text
            flashcards = generate_flashcards(pdf_text)

            response = get_response(pdf_text)
            st.session_state['chat_history'].append(("You", "PDF Text"))

            bot_response = response

            # Translate bot response to selected language
            translated_response = translator.translate(bot_response, dest=selected_language).text

            st.session_state['chat_history'].append(("BOT", translated_response))
            st.write(translated_response)

            # Store last response in session state
            st.session_state['last_response'] = translated_response

            # Playable Audio Response for translated text
            audio_file = speak(translated_response, lang=selected_language)
            if audio_file:
                st.audio(audio_file, format="audio/mp3")

    # Display Flashcards
    if flashcards:
        st.subheader("📚 Flashcards")
        flashcard_index = random.randint(0, len(flashcards) - 1)
        flashcard = flashcards[flashcard_index]

        with st.expander(f"Q: {flashcard['question']}"):
            st.write(f"A: {flashcard['answer']}")

# Display chat history
st.subheader("📜 Recent Queries:")
for role, text in st.session_state['chat_history']:
    st.markdown(f"{role}: {text}")

# Button to listen to the last response again
if 'last_response' in st.session_state and st.button("🔊 Listen Again"):
    audio_file = speak(st.session_state['last_response'], lang=selected_language)
    if audio_file:
        st.audio(audio_file, format="audio/mp3")
