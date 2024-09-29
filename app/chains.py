import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


class Chain():
    def __init__(self, api_key, model_name='llama-3.1-70b-versatile',temperature=0.5, max_tokens=8000):
        
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
    
    def write_mail(self, job, links):
        
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Yuval, a computer science student looking to apply for a job.
            Your job is to write a compelling cold email to the hiring manager regarding the job mentioned above, 
            highlighting your capability in fulfilling their needs. 
            Emphasize your relevant skills, experiences, and enthusiasm for the role.
            Also, add the most relevant ones from the following links to showcase your portfolio: {link_list}
            Remember you are Yuval, a computer science student.
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
         
        chain_email = prompt_email | self.llm
        
        res = chain_email.invoke(input={'job_description': job, 'link_list': links})
        return res.content
        


if __name__ == '__main__':
    api_key = os.getenv('API_KEY')
    print(api_key)
        
        
        
        
        
        
        
        
        