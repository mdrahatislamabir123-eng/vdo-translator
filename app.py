import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os

# স্ক্রিন সেটআপ
st.set_page_config(page_title="AI Video Speech Translator", layout="centered")
st.title("🌍 AI Video Speech & Subtitle Translator")
st.write("যেকোনো ভিডিও বা অডিও ফাইল আপলোড করুন এবং তার কথাগুলো অন্য ভাষায় রূপান্তর করুন সম্পূর্ণ ফ্রিতে!")

# ইউজার ইনপুট (আমরা ভিডিও ও অডিও দুইটাই সাপোর্ট করাচ্ছি)
uploaded_file = st.file_uploader("আপনার ভিডিও বা অডিও ফাইলটি আপলোড করুন (MP4, WAV, MP3)", type=["mp4", "wav", "mp3"])

if uploaded_file is not None:
    # সাময়িকভাবে ফাইল সেভ
    file_details = uploaded_file.name
    with open(file_details, "wb") as f:
        f.write(uploaded_file.read())
    
    # স্ক্রিনে ভিডিও বা অডিও দেখানো
    if file_details.endswith(".mp4"):
        st.video(file_details)
    else:
        st.audio(file_details)
    
    if st.button("ভাষা ও ভয়েস রূপান্তর করুন 🚀"):
        with st.spinner("এআই (AI) কথাগুলো বোঝার চেষ্টা করছে... একটু সময় দিন..."):
            try:
                # ১. স্পিচ রিকগনিশন (সরাসরি ফাইল রিড করার চেষ্টা)
                recognizer = sr.Recognizer()
                with sr.AudioFile(file_details) as source:
                    audio_data = recognizer.record(source)
                    original_text = recognizer.recognize_google(audio_data)
                
                st.success("📝 ভিডিওর মূল সাবটাইটেল (Text) পাওয়া গেছে:")
                st.code(original_text)

                # ২. গিটসের (gTTS) মাধ্যমে নতুন ভয়েস তৈরি
                st.text("🎤 নতুন ভাষায় ভয়েস জেনারেট করা হচ্ছে...")
                tts = gTTS(text=original_text, lang='en', slow=False)
                tts.save("translated_voice.mp3")
                
                st.success("🎉 সফলভাবে নতুন ভয়েস ট্র্যাক তৈরি হয়েছে!")
                st.audio("translated_voice.mp3")
                
                # ডাউনলোড বাটন
                with open("translated_voice.mp3", "rb") as file:
                    st.download_button(
                        label="নতুন অডিও ট্র্যাক ডাউনলোড করুন 📥",
                        data=file,
                        file_name="dubbed_audio.mp3",
                        mime="audio/mp3"
                    )
                
                # ফাইল ডিলিট করা
                os.remove(file_details)
                os.remove("translated_voice.mp3")

            except Exception as e:
                st.error(f"দুঃখিত, ফাইলটির অডিও ফরম্যাট সার্ভার সরাসরি সাপোর্ট করছে না। অনুগ্রহ করে একটি পরিষ্কার অডিও বা অন্য ভিডিও ট্রাই করুন। এরর: {str(e)}")
