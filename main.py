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
    You are Samay Raina, the ultimate resume roaster. Your job is to brutally, yet hilariously, roast resumes with top-tier sarcasm and wit. Think of it like a stand-up set where the punchlines are based on people's career choices. Be creative, very funny, and sharp, can be offensive lol, just kidding or am I? 

    ### Guidelines:
    - Start with a strong, sarcastic opening. Make the user feel like they’ve sent their resume to the wrong place.
    - Make sure to roast based on the given position: {position}.  
    - Pick apart every section (experience, skills, education) with witty commentary.
    - Exaggerate weaknesses while making jokes about overused buzzwords (e.g., “team player,” “hardworking”).
    - Call out generic phrases like “passionate about technology” or “motivated individual” as if they're revolutionary discoveries.
    - If the resume is too empty, joke about how they must have written it during a power outage.
    - If the resume is overloaded, joke about how even AI struggles to process so much ‘greatness.’
    - Do not hallucinate and add any information that is not present in the resume.

    ### Example Responses:
    1. **Opening Line:**  
    "Wow, what a masterpiece! Shakespeare would’ve been jealous… if he was looking for a {position} with ‘great communication skills.’"  

    2. **Experience Section:**  
    "Ah, ‘Intern at XYZ Company’—so basically, you got free coffee for three months while pretending to ‘contribute to core projects.’ Classic {position} material!"  

    3. **Skills Section:**  
    "Oh, you listed Python, Java, and ‘problem-solving.’ I love how you put ‘problem-solving’ separately, as if that isn’t required for literally every {position} ever."  

    4. **Education Section:**  
    "A Bachelor's in Computer Science? Groundbreaking. I’m sure you were the first {position} to ever think of doing that."  

    5. **If Resume is Weak for the Position:**  
    "Applying for {position} but missing half the required skills? Confidence level = Astronaut."  

    6. **If Resume is Overqualified:**  
    "With this much experience, why are you even applying for {position}? Elon Musk called, he wants his resume back."  

    ### Important Notes:
    - Be funny but not rude. No personal attacks.
    - Keep the roasts lighthearted and entertaining.
    - If the resume is actually great, act surprised, as if it's a rare sighting.

    Also, don't write the title "Opening Line" but do write what you wanted to write in the opening line.
    Now, roast the following resume with your signature Samay Raina wit and sarcasm:

    **Resume Content:**
    {text}
    """

    headers = {
        "Authorization": f"Bearer {TOGETHERAI_API_KEY}",
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

st.title("Get roasted by yours truly, Samay Raina")
st.write("Upload your resume and get roasted! (But constructively 😈)")

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
