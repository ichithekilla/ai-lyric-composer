import streamlit as st
import openai

st.set_page_config(page_title="AI Lyric Composer", layout="centered")

st.title("🎵 AI Lyric Composer")

import os
openai.api_key = os.getenv("OPENAI_API_KEY")

theme = st.text_input("Song Theme / Mood / First Line", placeholder="e.g. heartbreak in the rain")
structure = st.radio("Song Structure", ["Just Verses", "Verse and Chorus", "Custom"], index=1)
custom_structure = ""
if structure == "Custom":
    custom_structure = st.text_area("Custom Structure (e.g. Verse, Pre-Chorus, Chorus)", height=70)

if st.button("Generate Lyrics"):
    if not theme:
        st.error("Please enter a song theme/mood/line.")
    else:
        prompt = f"Write original and creative lyrics for a song about '{theme}'."
        if structure == "Verse and Chorus":
            prompt += "\nOrganize the lyrics with labeled [Verse] and [Chorus] sections."
        elif structure == "Custom" and custom_structure.strip():
            prompt += f"\nUse this song structure: {custom_structure.strip()}."
        else:
            prompt += "\nWrite several verses."
        prompt += "\nMake sure the lyrics are creative, not repetitive, and match the theme."

        with st.spinner("Generating lyrics..."):
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=400,
                    temperature=0.95,
                )
                lyrics = response.choices[0].message.content
                st.subheader("Generated Lyrics")
                st.text_area("Lyrics", value=lyrics, height=350)
            except Exception as e:
                st.error(f"Error: {e}")
