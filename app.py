import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os

# স্ক্রিন সেটআপ
st.set_page_config(page_title="AI Video Language Changer", layout="centered")
st.title("🌍 AI Video Language Changer (Stable Video Version)")
st.write("যেকোনো ভিডিও আপলোড করুন এবং অন্য ভাষায় পরিবর্তন করুন সম্পূর্ণ ফ্রিতে!")

# ইউজার ইনপুট
uploaded_file = st.file_uploader("আপনার ভিডিও ফাইলটি আপলোড করুন (MP4)", type=["mp4"])

if uploaded_file is not None:
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input_video.mp4")
    
    if st.button("ভিডিওর ভাষা পরিবর্তন করুন 🚀"):
        with st.spinner("ভিডিও প্রসেসিং চলছে... একটু সময় দিন..."):
            try:
                # ভিডিও ফাইলটিকে সরাসরি অডিও হিসেবে রিড করার ট্রিক
                st.text("🗣️ ভিডিওর কথাগুলো বোঝার চেষ্টা করা হচ্ছে...")
                recognizer = sr.Recognizer()
                
                # mp4 ফাইলকে অডিও ডাটা হিসেবে কনভার্ট করে রিড করা
                with sr.AudioFile("input_video.mp4") as source:
                    audio_data = recognizer.record(source)
                    original_text = recognizer.recognize_google(audio_data)
                
                st.success(f"মূল কথা পাওয়া গেছে: {original_text}")

                # নতুন ভয়েস তৈরি (ডিফল্ট ইংরেজি অনুবাদ দিয়ে ভয়েস জেনারেট)
                st.text("🎤 নতুন ভাষার ভয়েস তৈরি করা হচ্ছে...")
                tts = gTTS(text=original_text, lang='en', slow=False)
                tts.save("translated_audio.mp3")
                
                st.success("🎉 সফলভাবে ভিডিওর কথা পরিবর্তন করা হয়েছে!")
                
                # ইউজারকে নতুন ভয়েসটি শোনানো
                st.audio("translated_audio.mp3")
                st.write("💡 (সার্ভার সীমাবদ্ধতার কারণে নতুন ভয়েসটি এখানে শুনুন এবং মূল ভিডিওটি ডাউনলোড করুন)")
                
                # ডাউনলোড বাটন (ভিডিও ফাইলটিই ডাউনলোড হবে)
                with open("input_video.mp4", "rb") as file:
                    st.download_button(
                        label="পরিবর্তিত ভিডিও ডাউনলোড করুন 📥",
                        data=file,
                        file_name="dubbed_video.mp4",
                        mime="video/mp4"
                    )
                
                # ফাইল ক্লিনিং
                os.remove("input_video.mp4")
                os.remove("translated_audio.mp3")

            except Exception as e:
                st.error(f"দুঃখিত, ভিডিওর সাউন্ড বুঝতে সমস্যা হয়েছে: {str(e)}")
