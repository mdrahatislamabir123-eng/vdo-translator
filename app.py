import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import speech_recognition as sr
import os

# পেজ সেটআপ
st.set_page_config(page_title="AI Audio Dubber", layout="centered")
st.title("🎙️ AI Audio Dubber & Language Changer")
st.write("আপনার ভিডিওর অডিও ফাইলটি (MP3/WAV) এখানে আপলোড করুন এবং যেকোনো ভাষায় ডাব করুন!")

# ভাষার তালিকা
language_options = {name.title(): code for code, name in LANGUAGES.items()}

# ইনপুট
uploaded_file = st.file_uploader("আপনার অডিও ফাইলটি আপলোড করুন", type=["mp3", "wav"])
target_lang_name = st.selectbox("কোন ভাষায় ডাব করতে চান?", list(language_options.keys()))
target_lang_code = language_options[target_lang_name]

if uploaded_file is not None:
    # ফাইল সেভ করা
    with open("temp_audio.wav", "wb") as f:
        f.write(uploaded_file.read())
    
    st.audio("temp_audio.wav")
    
    if st.button("ডাবিং শুরু করুন 🚀"):
        with st.spinner("এআই আপনার কথাগুলো শুনছে ও অনুবাদ করছে..."):
            try:
                # ১. কথা শোনা
                recognizer = sr.Recognizer()
                with sr.AudioFile("temp_audio.wav") as source:
                    audio_data = recognizer.record(source)
                    original_text = recognizer.recognize_google(audio_data)
                
                st.success(f"🗣️ মূল কথা চেনা গেছে: {original_text}")

                # ২. অনুবাদ
                translator = Translator()
                translated = translator.translate(original_text, dest=target_lang_code)
                translated_text = translated.text
                st.success(f"🔄 অনূদিত কথা ({target_lang_name}): {translated_text}")

                # ৩. নতুন ডাবিং ভয়েস তৈরি
                tts = gTTS(text=translated_text, lang=target_lang_code, slow=False)
                tts.save("dubbed_voice.mp3")
                
                st.success("🎉 আপনার ডাব করা নতুন অডিও ট্র্যাক তৈরি!")
                st.audio("dubbed_voice.mp3")
                
                # ডাউনলোড বাটন
                with open("dubbed_voice.mp3", "rb") as file:
                    st.download_button(
                        label="ডাব করা অডিও ডাউনলোড করুন 📥",
                        data=file,
                        file_name=f"dubbed_{target_lang_name}.mp3",
                        mime="audio/mp3"
                    )
                
                # ফাইল ডিলিট
                os.remove("temp_audio.wav")
                os.remove("dubbed_voice.mp3")

            except Exception as e:
                st.error(f"দুঃখিত, কথাটি বুঝতে সমস্যা হয়েছে। দয়া করে স্পষ্ট কণ্ঠের ফাইল আপলোড করুন। এরর: {str(e)}")
