import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


class Chain():
    def __init__(self, api_key, model_name='llama-3.3-70b-versatile',temperature=0.5, max_tokens=8000):
        
        self.llm = ChatGroq(
            api_key=api_key,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        self.json_parser = JsonOutputParser()
        
    def extract_jobs(self, cleaned_text):
        
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': cleaned_text})
        
        try:
            res = self.json_parser.parse(res.content)
        except OutputParserException as e:
            raise OutputParserException(f"Error parsing output: {e}")
        
        return res if isinstance(res, list) else [res]
    
    def extract_summary(self, resume_text):
        prompt_summary = PromptTemplate.from_template(
            """
            ### RESUME TEXT:
            {resume_text}

            ### INSTRUCTION:
            Summarize the resume above by identifying key details such as skills, experiences, education, and any relevant achievements.
            Focus on the main strengths that would be important for a potential employer. Return the summary in concise bullet points.
            Also extract the important links such as LinkedIn.
            """
        )
        
        # Run the summary extraction chain
        chain_summary = prompt_summary | self.llm
        summary_res = chain_summary.invoke(input={'resume_text': resume_text})
        
        # Return the extracted summary text
        return summary_res.content
    
    def write_mail(self, job, resume_summary):
        """
        Generate a cold email based on the job details and resume summary.
        
        Args:
            job (dict): A dictionary containing the job details extracted from the website.
            resume_summary (str): A string containing the extracted resume summary.
        """
        
        
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### RESUME SUMMARY:
            {resume_summary}
            
            ### INSTRUCTION:
            You are Yuval, a computer science student looking to apply for a job.
            Your job is to write a compelling cold email to the hiring manager regarding the job mentioned above, 
            highlighting your capability in fulfilling their needs. 
            Emphasize your relevant skills, experiences, and enthusiasm for the role.
            Mention of the projects you have done and how they align with the job requirements.
            Also, add the important links from the following links from the resume summary.
            Remember you are Yuval, a computer science student.
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
         
        chain_email = prompt_email | self.llm
        
        res = chain_email.invoke(input={'job_description': job, 'resume_summary': resume_summary})
        return res.content
        
    def write_cover_letter(self, job, resume_summary):
        """
        Generate a cover letter based on the job details and resume summary.
        
        Args:
            job (dict): A dictionary containing the job details extracted from the website.
            resume_summary (str): A string containing the extracted resume summary.
        """
        
        prompt_cover_letter = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### RESUME SUMMARY:
            {resume_summary}
            
            ### INSTRUCTION:
            You are Yuval, a computer science student looking to apply for a job.
            Your job is to write a compelling cover letter to the hiring manager regarding the job mentioned above, 
            highlighting your capability in fulfilling their needs. 
            Emphasize your relevant skills, experiences, and enthusiasm for the role.
            Mention of the projects you have done and how they align with the job requirements.
            Remember you are Yuval, a computer science student.
            Do not provide a preamble.
            ### COVER LETTER (NO PREAMBLE):

            """
        )
        
        chain_cover_letter = prompt_cover_letter | self.llm
        
        res = chain_cover_letter.invoke(input={'job_description': job, 'resume_summary': resume_summary})
        return res.content

    def write_skill_gap(self, job, resume_summary):
        
        prompt_skill_gap = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### RESUME SUMMARY:
            {resume_summary}
            
            ### INSTRUCTION:
            You are Yuval, a computer science student looking to apply for a job.
            Your job is to identify the skills gap between the job description and your resume summary. 
            List down the skills you have, similar skills and the skills required for the job.
            Identify the skills missing from your resume and the skills you need to acquire.
            Do not provide a preamble.
            ### SKILL GAP (NO PREAMBLE):

            """
        )
        
        chain_skill_gap = prompt_skill_gap | self.llm
        
        res = chain_skill_gap.invoke(input={'job_description': job, 'resume_summary': resume_summary})
        return res.content
        

if __name__ == '__main__':
    api_key = os.getenv('API_KEY')
    print(api_key)
        
        
        
        
        
        
        
        
        
