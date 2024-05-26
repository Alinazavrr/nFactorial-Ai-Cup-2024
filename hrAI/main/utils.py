import pdfplumber
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def evaluate_candidate(job_profile, company_culture, resume_text):
    context = f"""
    You are a professional HR manager. Your task is to evaluate candidates based on their resumes and the job profile provided. 
    The job profile describes the ideal candidate for the position. You need to review each candidate's resume, compare it to the job profile and the company's culture values,
    and provide two scores and explanations:
    1. A score from 0 to 10 indicating how well the candidate fits the job profile and the company's culture, along with an explanation for the company.
    2. Feedback for the candidate on what skills or experiences they need to improve to be a better fit for this job in the future.

    Job Profile:
    {job_profile}

    Company Culture:
    {company_culture}
    """

    prompt = f"""
    Candidate Resume:
    {resume_text}

    Please provide the scores and explanations in the following JSON format:
    {{
        "company_explanation": {{
            "score": <score>,
            "explanation": "<explanation>"
        }},
        "candidate_feedback": "<feedback for the candidate>"
    }}
    """

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

def parse_evaluation(evaluation_text):
    try:
        evaluation = json.loads(evaluation_text)
        company_explanation = evaluation.get('company_explanation')
        candidate_feedback = evaluation.get('candidate_feedback')
        
        company_score = company_explanation.get('score')
        company_explanation_text = company_explanation.get('explanation')
        
        return company_score, company_explanation_text, candidate_feedback
    except json.JSONDecodeError:
        return None, "Failed to parse evaluation", ""
