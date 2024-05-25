# hr/utils.py
from openai import OpenAI 
from dotenv import load_dotenv
import pdfplumber
import json
import os
load_dotenv()

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text


def evaluate_candidate(job_profile, resume_text):
    context = f"""
    You are a professional HR manager. Your task is to evaluate candidates based on their resumes and the job profile provided. 
    The job profile describes the ideal candidate for the position. You need to review each candidate's resume, compare it to the job profile,
    and provide a score from 0 to 100 indicating how well the candidate fits the job profile. A score above 70 means the candidate is considered 
    suitable for the job. Additionally, provide a brief explanation justifying your score.

    Job Profile:
    {job_profile}
    """

    prompt = f"""
    Candidate Resume:
    {resume_text}

    Please provide the score and a brief explanation in the following JSON format:
    {{
        "score": <score>,
        "explanation": "<explanation>"
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
        score = evaluation.get('score')
        explanation = evaluation.get('explanation')
        return score, explanation
    except json.JSONDecodeError:
        return None, "Failed to parse evaluation"
