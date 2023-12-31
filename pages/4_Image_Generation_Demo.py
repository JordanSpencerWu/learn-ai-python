import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Image Generation Demo")

with st.form("image_generation_form"):
    prompt = st.text_input("Enter text prompt for image generation")
    size = st.selectbox(
        "Select image size", options=("256x256", "512x512", "1024x1024"), index=0
    )
    num_of_images = st.selectbox("Select number of images", options=(1, 2, 3), index=0)

    submitted = st.form_submit_button("Generate Image")
    if submitted:
        prompt = prompt.strip()
        if prompt:
            images = openai.Image.create(prompt=prompt, size=size, n=num_of_images)
            for image in images["data"]:
                st.image(image["url"])
        else:
            st.error("Please enter text prompt", icon="🚨")
