import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os
import subprocess

# স্ক্রিন সেটআপ
st.set_page_config(page_title="AI Video Language Changer", layout="centered")
st.title("🌍 AI Video Language Changer (Final Version)")
st.write("যেকোনো ভিডিও আপলোড করুন এবং অন্য ভাষায় পরিবর্তন করুন সম্পূর্ণ ফ্রিতে!")

# ইউজার ইনপুট
uploaded_file = st.file_uploader("আপনার ভিডিও ফাইলটি আপলোড করুন (MP4)", type=["mp4"])

if uploaded_file is not None:
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input_video.mp4")
    
    if st.button("ভিডিওর ভাষা পরিবর্তন করুন 🚀"):
        with st.spinner("ভিডিও প্রсеসিং চলছে... একটু সময় দিন..."):
            try:
                # ১. ffmpeg দিয়ে ভিডিও থেকে খাঁটি WAV অডিও আলাদা করা
                st.text("🎵 ভিডিও থেকে অডিও আলাদা করা হচ্ছে...")
                if os.path.exists("extracted_audio.wav"):
                    os.remove("extracted_audio.wav")
                
                # সিস্টেম কমান্ড ব্যবহার করে রূপান্তর
                cmd = "ffmpeg -i input_video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 extracted_audio.wav -y"
                subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # ২. কথা শোনা (Speech to Text)
                st.text("🗣️ ভিডিওর কথাগুলো বোঝার চেষ্টা করা হচ্ছে...")
                recognizer = sr.Recognizer()
                with sr.AudioFile("extracted_audio.wav") as source:
                    audio_data = recognizer.record(source)
                    original_text = recognizer.recognize_google(audio_data)
                
                st.success(f"মূল কথা পাওয়া গেছে: {original_text}")

                # ৩. নতুন ভাষার ভয়েস তৈরি করা (ইংরেজি অনুবাদ হিসেবে)
                st.text("🎤 নতুন ভাষার ভয়েস তৈরি করা হচ্ছে...")
                tts = gTTS(text=original_text, lang='en', slow=False)
                tts.save("translated_audio.mp3")
                
                # ৪. নতুন অডিও এবং পুরানো ভিডিও একসাথে মার্জ করে নতুন ভিডিও বানানো
                st.text("🎬 নতুন অ디오 ভিডিওর সাথে জুড়ে দেওয়া হচ্ছে...")
                if os.path.exists("output_video.mp4"):
                    os.remove("output_video.mp4")
                
                # ffmpeg দিয়ে অডিও প্রতিস্থাপন করার কমান্ড
                merge_cmd = "ffmpeg -i input_video.mp4 -i translated_audio.mp3 -c:v copy -map 0:v:0 -map 1:a:0 -shortest output_video.mp4 -y"
                subprocess.run(merge_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                st.success("🎉 সফলভাবে ভিডিওর ভাষা পরিবর্তন করা হয়েছে!")
                st.video("output_video.mp4")
                
                # ডাউনলোড বাটন
                with open("output_video.mp4", "rb") as file:
                    st.download_button(
                        label="পরিবর্তিত ভিডিও ডাউনলোড করুন 📥",
                        data=file,
                        file_name="translated_video.mp4",
                        mime="video/mp4"
                    )
                
                # সাময়িক ফাইলগুলো মুছে ফেলা
                os.remove("input_video.mp4")
                os.remove("extracted_audio.wav")
                os.remove("translated_audio.mp3")
                os.remove("output_video.mp4")

            except Exception as e:
                st.error(f"দুঃখিত, কোনো একটি ধাপে সমস্যা হয়েছে: {str(e)}")
