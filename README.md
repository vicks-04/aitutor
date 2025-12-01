# aitutor
GENMIND AI is a Streamlit-based study assistant that accepts text or PDF, extracts key information, and generates answers using Gemini AI. It supports multilingual translation, text-to-speech, and auto flashcard creation, helping users learn quickly with an interactive and smart study interface.
🧠 GENMIND AI – Code Description

This application is a Streamlit-based AI Study Assistant that can:

✔ Take text input
✔ Accept PDF upload
✔ Extract text from PDF
✔ Generate AI responses using Google Gemini
✔ Translate responses into multiple languages
✔ Convert text to speech (TTS)
✔ Create simple automated flashcards
✔ Maintain chat history

🔧 IMPORTS & SETUP
Libraries Used

streamlit → UI framework

google.generativeai → Gemini API

gTTS → Convert text to speech

BytesIO → Create in-memory audio file

PyPDF2 → Extract text from PDF

random → Pick random flashcards

googletrans → Translate text

API Configuration
api_key = 'AIzaSy...'
genai.configure(api_key=api_key)


Sets your Gemini API key and configures access.

Translator Instance

A global translator object for multilingual output.

🧠 FUNCTIONS
1️⃣ get_response(input_text)

Sends the user's question to Gemini and returns the final generated response.
Uses response.resolve() so streaming is fully collected before reading.

2️⃣ speak(text, lang)

Converts AI response into an audio file using gTTS.
Returns an in-memory MP3 file so Streamlit can play it instantly.

3️⃣ extract_text_from_pdf(pdf_file)

Reads PDF file page by page and extracts raw text using PyPDF2.

4️⃣ generate_flashcards(text)

Creates simple flashcards using predefined questions such as:

What is the main concept?

Explain the key idea.

For each question, it asks Gemini and stores a Q & A pair.

🎨 STREAMLIT UI SETUP
Page Title & Header

Shows app name on the top.

💬 CHAT SESSION INITIALIZATION

Uses Gemini’s start_chat() feature to maintain conversation context.

📌 Language Options

A dropdown menu allowing the user to choose the output speech language (English, Hindi, Telugu, Spanish…).

✍️ INPUT MODE (Text or PDF)

User selects how they want to input data:

✔ Text Mode → type your question
✔ PDF Mode → upload a PDF
🚀 SUBMIT ACTION

When user clicks Submit, one of two workflows happens:

📄 A) TEXT MODE WORKFLOW

Take the user’s question

Send request to Gemini

Save the conversation history

Translate AI response

Convert translated response to speech

Generate flashcards

Display everything

📘 B) PDF MODE WORKFLOW

Extract text from the PDF

Display extracted text

Create flashcards using extracted text

Send entire PDF text to Gemini

Translate response

Convert to speech

Display flashcards

🧾 FLASHCARDS

Shows one randomly selected flashcard in a collapsible container.

📜 RECENT QUERIES

Displays user messages + bot responses from session state.

🔊 LISTEN AGAIN

Replay last stored AI response in audio form.

✅ APP FINISHES
⭐ IN SHORT (Very Simple Description)

Your app:

Accepts Text or PDF

Uses Gemini to generate answers

Uses Google Translate to translate output

Uses gTTS to generate voice output

Generates flashcards

Maintains chat history

Displays & plays response

A complete multilingual PDF-aware AI assistant.
