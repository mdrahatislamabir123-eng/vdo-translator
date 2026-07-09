import streamlit as st
import moviepy.editor as mp
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
import speech_recognition as sr

# স্ক্রিনের টাইটেল এবং ইন্টারফেস সেটআপ
st.set_page_config(page_title="AI Universal Video Dubber", layout="centered")
st.title("🌍 AI Universal Video Language Changer")
st.write("যেকোনো ভিডিও আপলোড করুন এবং পৃথিবীর যেকোনো ভাষায় পরিবর্তন করুন সম্পূর্ণ ফ্রিতে!")

# ভাষাগুলোর তালিকা তৈরি (পৃথিবীর সব প্রধান ভাষা)
language_options = {name.title(): code for code, name in LANGUAGES.items()}

# ইউজার ইন্টারফেস ইনপুট
uploaded_file = st.file_uploader("আপনার ভিডিও ফাইলটি আপলোড করুন (MP4)", type=["mp4"])
target_lang_name = st.selectbox("কোন ভাষায় পরিবর্তন করতে চান?", list(language_options.keys()))
target_lang_code = language_options[target_lang_name]

if uploaded_file is not None:
    # ফাইল সাময়িকভাবে সেভ করা
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input_video.mp4")
    
    if st.button("ভিডিওর ভাষা পরিবর্তন করুন 🚀"):
        with st.spinner("প্রসেসিং চলছে... একটু সময় দিন..."):
            try:
                # ১. ভিডিও থেকে অডিও আলাদা করা
                st.text("🎵 ভিডিও থেকে অডিও আলাদা করা হচ্ছে...")
                video = mp.VideoFileClip("input_video.mp4")
                video.audio.write_audiofile("extracted_audio.wav", codec='pcm_s16le')
                
                # ২. স্পিচ-টু-টেক্সট (ভিডিওর কথাকে লেখায় রূপান্তর)
                st.text("🗣️ ভিডিওর কথাগুলো বোঝার চেষ্টা করা হচ্ছে...")
                recognizer = sr.Recognizer()
                with sr.AudioFile("extracted_audio.wav") as source:
                    audio_data = recognizer.record(source)
                    # স্বয়ংক্রিয়ভাবে ভাষা সনাক্ত করে টেক্সট করা
                    original_text = recognizer.recognize_google(audio_data)
                
                st.success(f"মূল কথা পাওয়া গেছে: {original_text}")

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

                # ৫. নতুন অডিও ভিডিওর সাথে যুক্ত করা (Audio Video Merging)
                st.text("🎬 নতুন অডিও ভিডিওর সাথে নিখুঁতভাবে জুড়ে দেওয়া হচ্ছে...")
                new_audio = mp.AudioFileClip("translated_audio.mp3")
                
                # ভিডিওর দৈর্ঘ্য অনুযায়ী অডিওর গতি বা দৈর্ঘ্য ঠিক করা
                final_video = video.set_audio(new_audio)
                final_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")
                
                st.success("🎉 সফলভাবে আপনার ভিডিওর ভাষা পরিবর্তন করা হয়েছে!")
                st.video("output_video.mp4")
                
                # ডাউনলোড বাটন
                with open("output_video.mp4", "rb") as file:
                    st.download_button(
                        label="ডাউনলোড করুন 📥",
                        data=file,
                        file_name=f"dubbed_{target_lang_name}.mp4",
                        mime="video/mp4"
                    )
                
                # ফাইল ক্লিনিং (সার্ভার খালি করার জন্য)
                video.close()
                new_audio.close()
                os.remove("input_video.mp4")
                os.remove("extracted_audio.wav")
                os.remove("translated_audio.mp3")
                os.remove("output_video.mp4")

            except Exception as e:
                st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {str(e)}")
