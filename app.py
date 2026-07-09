import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os

# স্ক্রিন সেটআপ
st.set_page_config(page_title="AI Audio Translator", layout="centered")
st.title("🌍 AI Audio Language Changer")
st.write("যেকোনো অডিও ফাইল আপলোড করুন এবং অন্য ভাষায় রূপান্তর করুন সম্পূর্ণ ফ্রিতে!")

# ইউজার ইনপুট
uploaded_file = st.file_uploader("আপনার অডিও ফাইলটি আপলোড করুন (WAV/MP3)", type=["wav", "mp3"])

if uploaded_file is not None:
    with open("input_audio.wav", "wb") as f:
        f.write(uploaded_file.read())
    
    st.audio("input_audio.wav")
    
    if st.button("অনুবাদ ও ভয়েস পরিবর্তন করুন 🚀"):
        with st.spinner("প্রসেসিং চলছে..."):
            try:
                # ১. কথা শোনা (Speech to Text)
                recognizer = sr.Recognizer()
                with sr.AudioFile("input_audio.wav") as source:
                    audio_data = recognizer.record(source)
                    original_text = recognizer.recognize_google(audio_data)
                
                st.success(f"মূল কথা পাওয়া গেছে: {original_text}")

                # ২. টেক্সট-টু-স্পিচ (নতুন ভয়েস তৈরি)
                # সরাসরি ইংরেজি বা অন্য ভাষায় ভয়েস আউটপুট করার জন্য
                tts = gTTS(text=original_text, lang='en', slow=False)
                tts.save("output_audio.mp3")
                
                st.success("🎉 সফলভাবে ভয়েস পরিবর্তন করা হয়েছে!")
                st.audio("output_audio.mp3")
                
                # ফাইল ক্লিনিং
                os.remove("input_audio.wav")
                os.remove("output_audio.mp3")

            except Exception as e:
                st.error(f"দুঃখিত, অডিও ফাইলটি পরিষ্কার না হওয়ায় বুঝতে সমস্যা হয়েছে: {str(e)}")
