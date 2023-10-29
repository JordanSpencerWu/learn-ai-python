import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]
openai_moderation_model = st.secrets["OPENAI_MODERATION_MODEL"]

st.set_page_config(page_title="Moderations Demo")

st.info(
    f"Using {openai_moderation_model} model to change modify OPENAI_MODERATION_MODEL in .streamlit/secrets.toml file",
    icon="ℹ️",
)


def generate_moderations(prompt):
    return openai.Moderation.create(input=prompt, model=openai_moderation_model)


prompt = """\
The less you give to me
The less you give to me
The less you give to me, the more I want it (Hey)

The less you give to me, the more I want it
You push me back until I'm two steps forward
But I can see the signs, recognise where we're going, so
The less you give to me, the more I want it

You know, I used to dream about this
I never thought it'd end up this way
The less you give to me the more I want
Drums

Drums
Drums
Da-da-da-da
Da-da-da-da
Da-da-da-da
Da-da-da-da (Hey)
Da-da-da-da
Da-da-da-da
The less you give to me the more I want it
(Hey)
(Never thought it would end up this way)
"""

with st.form("moderations_form"):
    prompt = st.text_area("Enter prompt:", prompt)

    submitted = st.form_submit_button("Generate Moderations")
    if submitted:
        moderations = generate_moderations(prompt)
        result = moderations["results"][0]
        flagged = result["flagged"]

        if flagged:
            st.error(f"Failed because of the following categories:")
            failed_categories = [
                category
                for category, flagged in result["categories"].items()
                if flagged
            ]
            for failed_category in failed_categories:
                st.error(failed_category)
        else:
            st.success(f"Passed")
