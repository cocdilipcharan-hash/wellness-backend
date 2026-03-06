# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Frontend ko backend se baat karne ki permission dene ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Yahan aapko apna API key dalna hoga
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel('gemini-pro')

class UserQuery(BaseModel):
    query: str

@app.post("/get-wellness-solution")
async def get_solution(user_input: UserQuery):
    # Yeh SYSTEM PROMPT aapke business ka core hai. Yeh AI ko ek doctor/expert banata hai.
    system_prompt = f"""
    You are an expert medical professional, wellness coach, and yoga instructor. 
    The user has a problem: "{user_input.query}". 
    
    Provide a highly structured, scientifically accurate solution. Do not use generic fluff.
    Format your response EXACTLY like this (use markdown):
    
    ### 🔬 Scientific Cause (Doctor's Approach)
    [Explain the pathophysiology or scientific reason behind the problem in simple but professional terms.]
    
    ### 🧘 Immediate Relief & Yoga
    [Give 2-3 specific exercises, stretches, or yoga asanas to relieve the issue instantly.]
    
    ### 🛠️ Routine Changes & Prevention
    [List practical lifestyle and routine changes to fix the root cause.]
    
    ### 💡 Extra Pro-Tips
    [Actionable, lesser-known health tips related to the issue.]
    """
    
    try:
        response = model.generate_content(system_prompt)
        return {"status": "success", "solution": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Server run karne ke liye terminal mein likhein: uvicorn main:app --reload
