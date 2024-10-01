import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from utils import clean_text, extract_text_from_pdf  # Assuming this is your function for extracting PDF text
import os
from dotenv import load_dotenv

load_dotenv()

def create_streamlit_app(llm, clean_text):
    st.title("📧 OutReachAce")

    # File uploader for resume
    resume_file = st.file_uploader("Upload your resume (PDF):", type=["pdf"])
    
    # Input for job URL
    url_input = st.text_input("Enter a Job URL:", value="https://jobs.nike.com/job/R-31388")

    # Checkbox for using only resume links
    use_resume_links_only = st.checkbox("Use only links from my resume")

    # Submit button
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Extract text from the uploaded resume PDF
            if resume_file is not None:
                resume_text = extract_text_from_pdf(resume_file)
                # Extract resume summary
                resume_summary = llm.extract_summary(resume_text)  # Extracted summary from the resume
            else:
                st.error("Please upload your resume PDF.")
                return

            # Load job data from the provided URL
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            # Extract job postings
            jobs = llm.extract_jobs(data)

            for job in jobs:

                st.markdown(f"### Job Title: {job['role']}")
                
                email = llm.write_mail(job, resume_summary=resume_summary, only_links=use_resume_links_only)
                st.code(email, language='markdown', wrap_lines=True)
                
                skill_gap = llm.write_skill_gap(job, resume_summary=resume_summary)
                st.code(skill_gap, language='markdown', wrap_lines=True)
                
                cover_letter = llm.write_cover_letter(job, resume_summary=resume_summary)
                st.code(cover_letter, language='markdown', wrap_lines=True)
                

        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain(os.getenv('API_KEY'), temperature=0.1, model_name='llama-3.1-70b-versatile')
    st.set_page_config(layout="wide", page_title="OutReachAce", page_icon="📧")
    create_streamlit_app(chain, clean_text)
