
import streamlit as st
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Personalized Industry Page", layout="centered")

# Load case studies
with open("case_studies.json") as f:
    case_studies = json.load(f)

st.title("🧠 Personalized Industry Page Generator")
st.caption("Powered by GPT + Agent42Labs + Apple UI Style")

name = st.text_input("Your Name")
email = st.text_input("Your Email")
prompt = st.text_area("Describe your request", placeholder="e.g. I'm in Healthcare and need expertise in migration")

if st.button("Generate Page"):
    if not name or not prompt:
        st.error("Please enter both name and prompt.")
    else:
        with st.spinner("Generating your personalized page..."):
            # Basic industry detection
            industry = "healthcare" if "healthcare" in prompt.lower() else "agritech" if "agri" in prompt.lower() else "general"

            # GPT Content
            user_prompt = f"Generate a personalized HTML page for a user named {name} interested in {industry}. The user said: {prompt}. Include a greeting, summary, and highlight 2-3 case studies. Make it look clean and professional like an Apple product site."
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_prompt}]
            )
            html = response.choices[0].message["content"]

            # Save to file
            filename = f"{name.lower().replace(' ', '_')}_{industry}.html"
            filepath = os.path.join("outputs", filename)
            os.makedirs("outputs", exist_ok=True)
            with open(filepath, "w") as f:
                f.write(html)

            # Display in app
            st.success("✅ Page generated! Preview below:")
            st.download_button("📄 Download HTML", html, file_name=filename, mime="text/html")
            st.components.v1.html(html, height=500, scrolling=True)
