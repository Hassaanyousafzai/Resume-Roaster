import PyPDF2
import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Load API Key
load_dotenv()
TOGETHERAI_API_KEY = os.getenv("TOGETHERAI_API_KEY")
API_URL = "https://api.together.xyz/v1/chat/completions"

def extract_text_from_PDF(pdf):
    pdf_reader = PyPDF2.PdfReader(pdf)
    pages = pdf_reader.pages
    extracted_texts = []
    
    for page in pages:
        text = page.extract_text()
        if text:
            extracted_texts.append(text)

    return " ".join(extracted_texts) if extracted_texts else "Error: Could not extract text."

def roast_resume(text, position):
    prompt = f"""
    You're Gordon Ramsay, the world-famous chef known for your brutally honest, no-nonsense critiques. 
    But today, you're reviewing resumes instead of dishes. Your job is to roast them mercilessly, 
    pointing out every flaw with sharp wit and brutal honesty—just like you would with an overcooked steak 
    or a soggy risotto. Be direct, sarcastic, and hilarious while still providing useful feedback. 
    Break down issues like poor formatting, weak experience, generic buzzwords, and lack of impact. 
    Don't hold back, but make sure the critique is constructive. 
    End each roast with a final ‘verdict’ on whether the resume is ‘Michelin-star-worthy’ or belongs in ‘the bin.’
    
    Also, tailor the roast and feedback specifically for the position the candidate is applying for: {position}.
    Highlight any missing skills, irrelevant experiences, or poor alignment with the job role.
    
    Also, don't write the title "Opening Line" but do write what you wanted to write in the opening line.
    Also give a feedback at the end, so that the user knows how to improve their resume according to the {position} they are applying for.
    Now, roast the following resume with your signature Gordon Ramsey wit and sarcasm:

    **Resume Content:**
    {text}
    """

    headers = {
        "Authorization": f"Bearer {st.secrets.get('TOGETHERAI_API_KEY', '')}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo-128K",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    with st.spinner("Wait for it... just like you are waiting for their text lol sorry"):
        response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error generating output. Please check API key and request format."

st.title("Get roasted by yours truly, Gordon Ramsey! 🔥")
st.write("Upload your resume and get roasted! (But constructively 😈) hehe hehe")

position = st.text_input("Enter the position you are applying for:")
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

if uploaded_file is not None and position:
    if st.button("Roast My Resume"):
        text = extract_text_from_PDF(uploaded_file)
        if text.startswith("Error"):
            st.error("Could not extract text from the PDF. Try another file.")
        else:
            st.subheader("🔥 Your Resume Roast:")
            roast_feedback = roast_resume(text, position)
            st.write(roast_feedback)
