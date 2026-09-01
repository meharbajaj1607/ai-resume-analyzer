AI Resume Analyzer
An AI-powered resume analyzer built using Python, Streamlit, and Gemini API.

Features
Upload resume as PDF
Extract resume text
Add target company and role
Upload job description
Analyze resume using Gemini
Identify strengths, weaknesses, and skill gaps
Generate ATS-relevant keywords
Get resume improvement suggestions
Tech Stack
Python
Streamlit
Gemini API
PyPDF
python-dotenv
Run Locally
pip install -r requirements.txt streamlit run app.py

Create a .env file: GEMINI_API_KEY=your_api_key

Output
The analyzer provides:

Overall Assessment
Strengths
Weaknesses
Missing Skills
Recommended Keywords
Resume Improvement Suggestions

```text
START
  |
User selects target
  |
Company-specific OR General
  |
If company-specific → enter company
  |
User selects role
  |
Role-specific OR General
  |
If role-specific → enter role
  |
User uploads resume
  |
Extract resume text
  |
Create dynamic prompt
  |
Send prompt + resume context to Gemini
  |
Receive analysis
  |
Display suggestions
  |
END
```

AI returns:
1. Overall Assessment
2. Strengths
3. Weaknesses
4. Missing Skills
5. Recommended Keywords
6. Resume Improvement Suggestions
