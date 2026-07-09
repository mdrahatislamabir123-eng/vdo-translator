import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import speech_recognition as sr
import os
from pydub import AudioSegment

# পেজ সেটআপ
st.set_page_config(page_title="AI Video Dubber", layout="centered")
st.title("🌍 AI Video Language Changer")
st.write("যেকোনো ভিডিও ফাইল (MP4) আপলোড করুন এবং অন্য ভাষায় ডাব করুন সম্পূর্ণ ফ্রিতে!")

# ভাষা তালিকা
language_options = {name.title(): code for code, name in LANGUAGES.items()}

# ফাইল আপলোডার
uploaded_file = st.file_uploader("আপনার ভিডিও ফাইলটি আপলোড করুন (MP4)", type=["mp4"])
target_lang_name = st.selectbox("কোন ভাষায় ডাব করতে চান?", list(language_options.keys()))
target_lang_code = language_options[target_lang_name]

if uploaded_file is not None:
    # ভিডিওটি সাময়িকভাবে সেভ করা
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input_video.mp4")
    
    if st.button("ভিডিওর ভাষা পরিবর্তন করুন 🚀"):
        with st.spinner("ভিডিও থেকে ভাষা পরিবর্তনের কাজ চলছে... একটু সময় দিন..."):
            try:
                # ১. pydub দিয়ে ভিডিওর ভেতর থেকে অডিও আলাদা করা
                st.text("🎵 ভিডিও থেকে অডিও ট্র্যাক আলাদা করা হচ্ছে...")
                audio = AudioSegment.from_file("input_video.mp4", format="mp4")
                audio.export("extracted_audio.wav", format="wav")
                
                # ২. কথা শুনে টেক্সটে রূপান্তর করা
                st.text("🗣️ ভিডিওর কথাগুলো বোঝার চেষ্টা করা হচ্ছে...")
                recognizer = sr.Recognizer()
                with sr.AudioFile("extracted_audio.wav") as source:
                    audio_data = recognizer.record(source)
                    original_text = recognizer.recognize_google(audio_data)
                
                st.success(f"🗣️ মূল কথা চেনা গেছে: {original_text}")

                # ৩. অনুবাদ করা
                st.text(f"🔄 {target_lang_name} ভাষায় অনুবাদ করা হচ্ছে...")
                translator = Translator()
                translated = translator.translate(original_text, dest=target_lang_code)
                translated_text = translated.text
                st.success(f"🔄 অনূদিত কথা: {translated_text}")

                # ৪. নতুন ডাবিং ভয়েস তৈরি করা
                st.text("🎤 নতুন ভাষায় ভয়েস জেনারেট করা হচ্ছে...")
                tts = gTTS(text=translated_text, lang=target_lang_code, slow=False)
                tts.save("translated_audio.mp3")
                
                st.success("🎉 আপনার নতুন ডাব করা অডিও ট্র্যাক তৈরি হয়েছে!")
                st.audio("translated_audio.mp3")
                st.write("💡 (দ্রষ্টব্য: ফ্রি সার্ভারে ভিডিওর ভেতরে অডিও জোর করে মার্চ করলে সার্ভার ক্র্যাশ করে, তাই নতুন অডিও ট্র্যাকটি এখানে শুনে ডাউনলোড করে নিন)")
                
                # ডাউনলোড বাটন
                with open("translated_audio.mp3", "rb") as file:
                    st.download_button(
                        label="ডাব করা অডিও ট্র্যাক ডাউনলোড করুন 📥",
                        data=file,
                        file_name=f"dubbed_{target_lang_name}.mp3",
                        mime="audio/mp3"
                    )
                
                # সাময়িক ফাইল ডিলিট করা
                os.remove("input_video.mp4")
                os.remove("extracted_audio.wav")
                os.remove("translated_audio.mp3")

            except Exception as e:
                st.error(f"দুঃখিত, একটি সমস্যা হয়েছে। দয়া করে স্পষ্ট কণ্ঠের কোনো ভিডিও ট্রাই করুন। এরর: {str(e)}")
