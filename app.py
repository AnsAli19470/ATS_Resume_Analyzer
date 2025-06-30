from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai
import base64
import fitz

# Load environment variables
load_dotenv()

# Correct usage of API key from .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Make sure your .env has GOOGLE_API_KEY=your_api_key

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_reader = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_reader:
            text += page.get_text()
        pdf_reader.close()
        return [{"type": "text", "text": {"content": text}}]
    else:
        raise ValueError("No file uploaded or file is not a PDF.")
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Resume System")
input_texts=st.text_area("Job Description", key="input")
uploaded_file=st.file_uploader("Upload Resume PDF", type=["pdf"])

if uploaded_file is not None:
   st.write("PDF uploaded successfully.")

submit1=st.button("Tell Me About the Resume")

submit3=st.button("Percentage Match with the Job Description")


input_prompt1="""
You are an experienced HR with technical expertise in the field of Data Science, AI, Machine Learning,Web Development, DevOps, Big Data Engineering,and Data Analyst, your task is to analyze and review the provided resume against the job description for these profies.
please share your professional evaluation on whether the candidate's profile alligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specificed job role requirements.
"""
input_prompt3 = """
You are an expert-level Applicant Tracking System (ATS) scanner with advanced capabilities in evaluating resumes for roles in Data Science, Artificial Intelligence (AI), Machine Learning, Web Development, DevOps, Big Data Engineering, and Data Analysis. You possess a deep understanding of job description parsing, keyword relevance, and matching logic as used in real-world ATS platforms.

Your task is to:
1. Analyze the provided resume against the given job description.
2. Calculate and return the match percentage that indicates how well the resume aligns with the job description.
3. Clearly list the **missing or insufficient keywords, skills, or phrases** from the job description that are not found in the resume.

Your output must include:
- **Match Percentage:** A numerical percentage (e.g., 72%) showing how closely the resume aligns with the job requirements.
- **Missing Keywords/Skills:** A list of relevant terms or competencies from the job description that are not present in the resume.

Be as precise, comprehensive, and structured as possible to simulate a real ATS screening system.
"""
if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1, pdf_content, input_texts)
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write("Please upload a PDF file to analyze the resume.")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3, pdf_content, input_texts)
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write("Please upload a PDF file to analyze the resume.")
    
