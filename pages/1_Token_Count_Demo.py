import tiktoken
import streamlit as st

st.set_page_config(page_title="Token Count Demo")

st.info(
    "Example of how to count the number of tokens. If you want to learn more about OpenAI Tokenizer check out https://platform.openai.com/tokenizer",
    icon="ℹ️",
)

default_prompt = """\
There was a time
I used to look into my father's eyes
In a happy home
I was a king, I had a golden throne
Those days are gone
Now they're memories on the wall
I hear the songs from the places where I was born
Up on a hill across the blue lake
That's where I had my first heartbreak
I still remember how it all changed
My father said
Don't you worry, don't you worry, child
See heaven's got a plan for you
Don't you worry, don't you worry now
Yeah
Don't you worry, don't you worry now
Yeah
Don't you worry, don't you worry now
Yeah
There was a time
I met a girl of a different kind
We ruled the world
I thought I'd never lose her out of sight
We were so young
I think of her now and then
I still hear the songs reminding me of a friend
Up on a hill across the blue lake
That's where I had my first heartbreak
I still remember how it all changed
My father said
Don't you worry, don't you worry, child
See heaven's got a plan for you
Don't you worry, don't you worry now
Yeah
Oh-oh-oh-oh-oh-oh-oh
Oh-oh-oh-oh-oh-oh-oh
Oh-oh-oh-oh-oh-oh-oh
Oh-oh-oh-oh-oh-oh-oh
Oh-oh-oh-oh-oh-oh-oh
Oh-oh-oh-oh-oh-oh-oh
Oh-oh-oh-oh-oh-oh-oh
See heaven's got a plan for you
See heaven's got a plan for you
See heaven's got a plan for you
Don't you worry, don't you worry, child
See heaven's got a plan for you
Don't you worry, don't you worry now
Yeah
Oh-oh-oh-oh-oh-oh-oh
Oh-oh-oh-oh-oh-oh-oh
Oh-oh-oh-oh-oh-oh-oh
Yeah
"""

enc = tiktoken.get_encoding("cl100k_base")

with st.form("token_count_form"):
    prompt = st.text_area("Enter prompt", value=default_prompt, height=450)

    submitted = st.form_submit_button("Count tokens")
    if submitted:
        prompt = prompt.strip()
        encoded_prompt = enc.encode(prompt)
        st.write(f"{len(encoded_prompt)} tokens")
