import openai
import tempfile
import streamlit as st
import os

from pydub import AudioSegment

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Speech To Text Demo")

OPENAI_ALLOWED_TYPES = [
    "flac",
    "m4a",
    "mp3",
    "mp4",
    "mpeg",
    "mpga",
    "ogg",
    "wav",
    "webm",
]

audio_file = st.file_uploader(
    "Upload an audio file",
    type=OPENAI_ALLOWED_TYPES,
)

if audio_file is not None:
    st.audio(audio_file, format=audio_file.type)

    submitted = st.button("Generate text from audio file")
    if submitted:
        # Save the uploaded audio data to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(audio_file.read())
        temp_file.close()

        # Load the temporary file using AudioSegment
        audio = AudioSegment.from_file(temp_file.name)

        # Clean up the temporary file
        os.remove(temp_file.name)

        # Export the processed audio to a new file
        one_minute = 1 * 60 * 1000
        first_one_minutes_of_song = audio[:one_minute]
        format = audio_file.type.split("/")[1]
        output_audio_path = f"output_processed_audio.{format}"
        first_one_minutes_of_song.export(output_audio_path, format=format)
        audio_data = open(output_audio_path, "rb")
        transacript = openai.Audio.translate("whisper-1", audio_data)
        st.info(transacript["text"])

        # Clean up the exported audio file when it's no longer needed
        if os.path.exists(output_audio_path):
            os.remove(output_audio_path)
