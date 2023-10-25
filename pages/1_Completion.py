import os
import openai
import streamlit as st

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
  page_title="Completion Demo"
)

def generate_response(prompt):
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
      ],
      temperature=0.6
    )
    st.info(completion.choices[0].message["content"])

zero_shot_prompt = """\
Classify the text into neutral, negative or positive. 
Text: I think the vacation is okay.
Sentiment:
"""

with st.form("my_form"):
  text = st.text_area("Enter text:", zero_shot_prompt)
  submitted = st.form_submit_button("Submit")
  if openai.api_key == None or not openai.api_key.startswith("sk-"):
    st.warning("Please source your OpenAI API Key!", icon="⚠")
  if submitted:
     generate_response(text)