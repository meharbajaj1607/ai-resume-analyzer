import streamlit as st
from pypdf import PdfReader
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# -------------------- UI / UX --------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="centered"
)

st.markdown("""
<style>
    /* ---------- Theme ---------- */

    .stApp {
        background-color: #F7E7B4;
        color: #4A2415;
    }

    .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    /* ---------- Typography ---------- */

    h1, h2, h3, p, label, span, div {
        color: #4A2415;
    }

    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        letter-spacing: -1px;
        margin-bottom: 0.25rem !important;
    }

    h3 {
        font-weight: 400 !important;
        opacity: 0.75;
        margin-bottom: 2rem !important;
    }

    /* ---------- File uploader ---------- */

    [data-testid="stFileUploader"] {
        background-color: #4A2415;
        border-radius: 14px;
        padding: 8px;
    }

    [data-testid="stFileUploader"] section {
        background-color: #4A2415;
        border: 2px dashed #F7E7B4;
        border-radius: 10px;
        padding: 25px;
    }

    [data-testid="stFileUploader"] * {
        color: #F7E7B4 !important;
    }

    [data-testid="stFileUploader"] button {
        background-color: #F7E7B4 !important;
        color: #4A2415 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* ---------- Radio buttons ---------- */

    [data-testid="stRadio"] label {
        color: #4A2415 !important;
    }

    /* ---------- Text inputs ---------- */

    .stTextInput input {
        background-color: #FFF4CF !important;
        color: #4A2415 !important;
        border: 1px solid #8B5E3C !important;
        border-radius: 8px !important;
    }

    .stTextInput input:focus {
        border: 2px solid #4A2415 !important;
        box-shadow: none !important;
    }

    /* ---------- Analyze button ---------- */

    .stButton > button {
        width: 100%;
        background-color: #4A2415 !important;
        color: #F7E7B4 !important;
        border: none !important;
        border-radius: 10px;
        padding: 0.7rem 1rem;
        font-size: 1rem;
        font-weight: 600;
    }

    .stButton > button p {
        color: #F7E7B4 !important;
    }

    .stButton > button:hover {
        background-color: #63351F !important;
        color: #F7E7B4 !important;
    }

    .stButton > button:hover p {
        color: #F7E7B4 !important;
    }

    /* ---------- Expanders ---------- */

    [data-testid="stExpander"] {
        background-color: #FFF4CF;
        border: 1px solid #D2B48C;
        border-radius: 10px;
    }

    /* ---------- Alerts ---------- */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* ---------- Divider ---------- */

    hr {
        border-color: #D2B48C;
    }

</style>
""", unsafe_allow_html=True)


# -------------------- Header --------------------

st.title("AI Resume Analyzer")
st.subheader("Analyze and improve your resume.")


# -------------------- Resume Upload --------------------

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)

resume_text = ""

if uploaded_file is not None:

    st.write("File name:", uploaded_file.name)
    st.write("File type:", uploaded_file.type)
    st.write("File size:", uploaded_file.size, "bytes")

    try:
        reader = PdfReader(uploaded_file)
        extracted_text = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                extracted_text.append(text)

        resume_text = "\n".join(extracted_text)

    except Exception:
        st.error("Unable to read this resume PDF.")
        st.stop()

    with st.expander("Resume Preview"):
        st.write(resume_text)


# -------------------- Company Selection --------------------

company = st.radio(
    "Target Company",
    ["General", "Company Specific"],
    horizontal=True
)

target_company = "General"

if company == "Company Specific":

    company_name = st.text_input(
        "Enter company name"
    )

    target_company = company_name


# -------------------- Role Selection --------------------

role = st.radio(
    "Target Role",
    ["General", "Role Specific"],
    horizontal=True
)

target_role = "General"

if role == "Role Specific":

    role_name = st.text_input(
        "Enter role name"
    )

    target_role = role_name


# -------------------- Job Description --------------------

jd = st.radio(
    "Add Job Description",
    ["Yes", "No"],
    horizontal=True
)

jd_text = ""

if jd == "Yes":

    jd_file = st.file_uploader(
        "Upload your job description",
        type=["pdf"],
        key="jd_uploader"
    )

    if jd_file is not None:

        st.write("File name:", jd_file.name)
        st.write("File type:", jd_file.type)
        st.write("File size:", jd_file.size, "bytes")

        try:
            reader_jd = PdfReader(jd_file)
            extracted_jd_text = []

            for page in reader_jd.pages:
                text = page.extract_text()

                if text:
                    extracted_jd_text.append(text)

            jd_text = "\n".join(extracted_jd_text)

        except Exception:
            st.error("Unable to read this job description PDF.")
            st.stop()

        with st.expander("Job Description Preview"):
            st.text(jd_text)


# -------------------- Analysis --------------------

st.divider()

if st.button("Analyze Resume"):

    # ---------- Validation ----------

    if uploaded_file is None:
        st.error("Please upload your resume.")
        st.stop()

    if not resume_text.strip():
        st.error(
            "No readable text could be extracted from this PDF. "
            "Please upload a text-based PDF."
        )
        st.stop()

    if company == "Company Specific" and not target_company.strip():
        st.error("Please enter a company name.")
        st.stop()

    if role == "Role Specific" and not target_role.strip():
        st.error("Please enter a role.")
        st.stop()

    if jd == "Yes" and not jd_text.strip():
        st.error(
            "Please upload a readable job description PDF."
        )
        st.stop()


    # -------------------- Prompt --------------------

    prompt = f"""
Role: Senior HR Manager and experienced technical recruiter and resume reviewer.

Task: Analyze and improve my resume.

Context:
Target Role: {target_role}
Target Company: {target_company}

Resume:
{resume_text}

Job Description:
{jd_text}

Constraints:
- Keep the analysis short and precise.
- If a specific company is given, tailor the analysis strictly according to that company.
- If a specific role is given, tailor the analysis strictly according to that role.
- If the target is general, identify suitable companies/roles based on the resume.
- Align the output with the job description when provided.
- Do not invent skills, experience, or achievements.
- Clearly state the skill gaps based on the target role and job description.
- Recommend skills that would help the candidate level up their existing skill set.
- Recommended keywords must be relevant to the target role and job description.
- Do not recommend irrelevant keywords simply to improve ATS matching.

Output:
Return the response using exactly these six headings
and do not add any other headings.

1. Overall Assessment: Give an overall score out of 10 and briefly explain it.
2. Strengths: Identify the strongest areas of the resume.
3. Weaknesses: Identify areas that need improvement.
4. Missing Skills: Identify skill gaps relevant to the target role and job description.
5. Recommended Keywords: Give relevant technical and role-specific keywords.
6. Resume Improvement Suggestions: Give practical suggestions to improve the resume.
"""


    # -------------------- Gemini --------------------

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error(
            "Gemini API key not found. "
            "Please add GEMINI_API_KEY to your .env file."
        )
        st.stop()

    try:

        client = genai.Client(
            api_key=api_key
        )

        with st.spinner("Analyzing your resume..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

        if response.text:
            st.subheader("Analysis")
            st.write(response.text)

        else:
            st.error(
                "The model did not return any analysis."
            )

    except Exception as e:

        st.error(
            "Something went wrong while analyzing your resume."
        )

        st.caption(
            f"Error details: {str(e)}"
        )
