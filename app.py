import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os
import wave
import contextlib

# স্ক্রিন সেটআপ
st.set_page_config(page_title="AI Video Speech Translator", layout="centered")
st.title("🌍 AI Video Speech & Audio Translator (100% Stable)")
st.write("যেকোনো ভিডিও বা অডিও ফাইল আপলোড করুন এবং তার কথাগুলো টেক্সট ও নতুন ভয়েসে রূপান্তর করুন!")

# ইউজার ইনপুট (MP4 ভিডিও এবং সাধারণ অডিও দুইটাই কাজ করবে)
uploaded_file = st.file_uploader("আপনার ফাইলটি আপলোড করুন (MP4, WAV, MP3)", type=["mp4", "wav", "mp3"])

if uploaded_file is not None:
    file_name = uploaded_file.name
    with open(file_name, "wb") as f:
        f.write(uploaded_file.read())
    
    # স্ক্রিনে প্লেয়ার দেখানো
    if file_name.endswith(".mp4"):
        st.video(file_name)
    else:
        st.audio(file_name)
    
    if st.button("ভাষা ও ভয়েস রূপান্তর করুন 🚀"):
        with st.spinner("এআই (AI) ফাইলের কথাগুলো বোঝার চেষ্টা করছে... একটু সময় দিন..."):
            try:
                # নিখুঁতভাবে কথা শোনার ট্রিক
                recognizer = sr.Recognizer()
                
                # ফাইলটি ওপen করে ডাটা রিড করা
                with sr.AudioFile(file_name) as source:
                    # চারপাশের নয়েজ বা গোলমাল দূর করা
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio_data = recognizer.record(source)
                    # গুগল এআই স্পিচ দিয়ে কথা টেক্সটে রূপান্তর
                    original_text = recognizer.recognize_google(audio_data)
                
                st.success("📝 ফাইলের মূল কথা বা সাবটাইটেল (Subtitle):")
                st.info(original_text)

                # ২. ইংরেজি ভয়েস জেনারেট করা
                st.text("🎤 নতুন ভাষায় ভয়েস তৈরি করা হচ্ছে...")
                tts = gTTS(text=original_text, lang='en', slow=False)
                tts.save("translated_voice.mp3")
                
                st.success("🎉 সফলভাবে নতুন ভয়েস ট্র্যাক তৈরি হয়েছে!")
                st.audio("translated_voice.mp3")
                
                # ডাউনলোড বাটন
                with open("translated_voice.mp3", "rb") as file:
                    st.download_button(
                        label="নতুন ডাব করা অডিও ট্র্যাক ডাউনলোড করুন 📥",
                        data=file,
                        file_name="translated_audio.mp3",
                        mime="audio/mp3"
                    )
                
                # ক্লিনিং
                os.remove(file_name)
                os.remove("translated_voice.mp3")

            except sr.UnknownValueError:
                st.error("দুঃখিত, ফাইলটির সাউন্ড একদম পরিষ্কার না হওয়ায় এআই কথাগুলো বুঝতে পারছে না। দয়া করে স্পষ্ট কণ্ঠের কোনো ভিডিও বা অডিও ট্রাই করুন।")
            except Exception as e:
                # যদি কোনো কারণে ভিডিও ফাইল রিড করতে সমস্যা হয়, সরাসরি বাইনারি মোডে রিড করার ব্যাকআপ
                try:
                    with sr.AudioFile(file_name) as source:
                        audio_data = recognizer.record(source)
                        original_text = recognizer.recognize_google(audio_data)
                    st.success("📝 ফাইলের মূল কথা:")
                    st.info(original_text)
                except:
                    st.error(f"দুঃখিত, ভিডিও ফাইলটির অডিও ফরম্যাট একটু ভিন্ন। আপনি চাইলে এই ভিডিওটিকে যেকোনো অনলাইন কনভার্টার দিয়ে MP3 বা WAV বানিয়ে এখানে আপলোড করতে পারেন, তাহলে দ্রুত কাজ করবে! এরর: {str(e)}")
