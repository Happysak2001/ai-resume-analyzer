import os
import streamlit as st
from groq import Groq

st.title("AI Resume Analyzer")
st.write("Paste your resume and job description below.")

# Input boxes
resume_text = st.text_area("Paste your Resume")
job_description = st.text_area("Paste Job Description")

# Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

if st.button("Analyze Resume"):
    if not resume_text or not job_description:
        st.warning("Please paste both resume and job description.")
    else:
        match_prompt = f"""
        You are a helpful AI resume reviewer.

        Compare the following resume with the job description.

        Return the response in this format:

        Match Summary:
        Write a short summary of how well the resume matches the job.

        Match Score:
        Give a score out of 10.

        Missing Skills or Keywords:
        List all important missing skills, tools, technologies, domain knowledge, and keywords that are present in the job description but missing or weak in the resume.

        Strengths:
        List the important strengths in the resume that match the job description.

        Suggestions:
        List all useful suggestions to improve the resume for this specific job. Do not limit the number of suggestions. Include technical, domain, keyword, and presentation improvements if relevant.

        Resume:
        {resume_text}

        Job Description:
        {job_description}
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": match_prompt}
            ],
            temperature=0.7
        )

        result = response.choices[0].message.content

        st.subheader("Analysis Result")
        st.write(result)