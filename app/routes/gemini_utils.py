import google.generativeai as genai
import time
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()


sys_instruction = """You are a document entity extraction specialist. Given a document related to a comprehensive sample paper, your task is to extract the following information in JSON format:
{
  "title": "",
  "type": "",
  "time": ,
  "marks": ,
  "params": {
    "board": "",
    "grade": ,
    "subject": ""
  },
  "tags": [
    "",
    ""
  ],
  "chapters": [
    "",
    ""
  ],
  "sections": [
    {
      "marks_per_question": "",
      "type": "",
      "questions": [
        {
          "question": "",
          "answer": "",
          "type": "",
          "question_slug": "",
          "reference_id": "",
          "hint": "",
          "params": {
            
          }
        },
        {
          "question": "",
          "answer": "",
          "type": "",
          "question_slug": "",
          "reference_id": "",
          "hint": "",
          "params": {
            
          }
        }
      ]
    }
  ]
}

please make sure not to give ```json in the beggining . the json should load as is .
"""

# Access the API key
api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)

# Configure Gemini model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=sys_instruction
)

# Helper functions
def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    return file

def wait_for_files_active(files):
    for file in files:
        while file.state.name == "PROCESSING":
            time.sleep(10)
            file = genai.get_file(file.name)
        if file.state.name != "ACTIVE":
            raise HTTPException(status_code=500, detail=f"File {file.name} failed to process")
