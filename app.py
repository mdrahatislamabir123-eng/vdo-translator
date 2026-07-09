import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import speech_recognition as sr
import os
import subprocess

# স্ক্রিন সেটআপ
st.set_page_config(page_title="AI Universal Video Dubber", layout="centered")
st.title("🌍 AI Universal Video Language Changer")
st.write("যেকোনো ভিডিও আপলোড করুন এবং পৃথিবীর যেকোনো ভাষায় পরিবর্তন করুন সম্পূর্ণ ফ্রিতে!")

# ভাষাগুলোর তালিকা তৈরি
language_options = {name.title(): code for code, name in LANGUAGES.items()}

# ইউজার ইন্টারফেস ইনপুট
uploaded_file = st.file_uploader("আপনার ভিডিও ফাইলটি আপলোড করুন (MP4)", type=["mp4"])
target_lang_name = st.selectbox("কোন ভাষায় পরিবর্তন করতে চান?", list(language_options.keys()))
target_lang_code = language_options[target_lang_name]

if uploaded_file is not None:
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input_video.mp4")
    
    if st.button("ভিডিওর ভাষা পরিবর্তন করুন 🚀"):
        with st.spinner("ভিডিও প্রসেসিং চলছে... একটু সময় দিন..."):
            try:
                # ১. ভিডিও থেকে অডিও আলাদা করা
                st.text("🎵 ভিডিও থেকে অডিও আলাদা করা হচ্ছে...")
                if os.path.exists("extracted_audio.wav"):
                    os.remove("extracted_audio.wav")
                
                cmd = "ffmpeg -i input_video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 extracted_audio.wav -y"
                subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # ২. কথা শোনা (Speech to Text)
                st.text("🗣️ ভিডিওর কথাগুলো বোঝার চেষ্টা করা হচ্ছে...")
                recognizer = sr.Recognizer()
                with sr.AudioFile("extracted_audio.wav") as source:
                    audio_data = recognizer.record(source)
                    original_text = recognizer.recognize_google(audio_data)
                
                st.success(f"मूल কথা পাওয়া গেছে: {original_text}")

                # ৩. অনুবাদ (Translation)
                st.text(f"🔄 {target_lang_name} ভাষায় অনুবাদ করা হচ্ছে...")
                translator = Translator()
                translated = translator.translate(original_text, dest=target_lang_code)
                translated_text = translated.text
                st.success(f"অনূদিত কথা: {translated_text}")

                # ৪. টেক্সট-টু-স্পিচ (নতুন ভয়েস তৈরি)
                st.text("🎤 নতুন ভাষার ভয়েস তৈরি করা হচ্ছে...")
                tts = gTTS(text=translated_text, lang=target_lang_code, slow=False)
                tts.save("translated_audio.mp3")
                
                # ৫. নতুন অডিও ভিডিওর সাথে মার্জ করা
                st.text("🎬 নতুন অডিও ভিডিওর সাথে জুড়ে দেওয়া হচ্ছে...")
                if os.path.exists("output_video.mp4"):
                    os.remove("output_video.mp4")
                
                merge_cmd = "ffmpeg -i input_video.mp4 -i translated_audio.mp3 -c:v copy -map 0:v:0 -map 1:a:0 -shortest output_video.mp4 -y"
                subprocess.run(merge_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                st.success("🎉 সফলভাবে ভিডিওর ভাষা পরিবর্তন করা হয়েছে!")
                st.video("output_video.mp4")
                
                # ডাউনলোড বাটন
                with open("output_video.mp4", "rb") as file:
                    st.download_button(
                        label="পরিবর্তিত ভিডিও ডাউনলোড করুন 📥",
                        data=file,
                        file_name=f"dubbed_{target_lang_name}.mp4",
                        mime="video/mp4"
                    )
                
                # ফাইল ক্লিনিং
                os.remove("input_video.mp4")
                os.remove("extracted_audio.wav")
                os.remove("translated_audio.mp3")
                os.remove("output_video.mp4")

            except Exception as e:
                st.error(f"দুঃখিত, কোনো একটি ধাপে সমস্যা হয়েছে: {str(e)}")
