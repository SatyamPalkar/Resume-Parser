from fastapi import FastAPI, File, UploadFile, HTTPException
import fitz
import docx
import re
import spacy
import json
from collections import defaultdict

app = FastAPI()
nlp = spacy.load('en_core_web_sm')

with open('skills.json', 'r') as f:
    skills_set = json.load(f)

def extract_text(file: UploadFile):
    if file.filename.lower().endswith('.pdf'):
        with fitz.open(stream=file.file.read(), filetype='pdf') as doc:
            text = ''.join(page.get_text() for page in doc)
    elif file.filename.lower().endswith('.docx'):
        doc = docx.Document(file.file)
        text = '\n'.join([para.text for para in doc.paragraphs])
    else:
        raise HTTPException(status_code=400, detail='Unsupported file type')
    return text

def extract_email(text):
    return re.findall(r'\b[\w.-]+?@\w+?\.\w+?\b', text)

def extract_phone(text):
    return re.findall(r'\+?\d[\d\s-]{8,}\d', text)

def extract_skills(text):
    return [skill for skill in skills_set if re.search(r'\b'+re.escape(skill.lower())+r'\b', text.lower())]

def extract_education(text):
    keywords = ['Bachelor', 'Master', 'B.Tech', 'M.Tech', 'PhD', 'University', 'College', 'Diploma']
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    return [sentence for sentence in sentences if any(keyword.lower() in sentence.lower() for keyword in keywords)]


@app.post("/parse_resume/")
async def parse_resume(file: UploadFile = File(...)):
    text = extract_text(file)
    parsed_data = defaultdict(list)
    parsed_data['email'] = extract_email(text)
    parsed_data['phone'] = extract_phone(text)
    parsed_data['skills'] = extract_skills(text)
    parsed_data['education'] = extract_education(text)
    return parsed_data
