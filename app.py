import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os
import urllib.parse
import urllib.request
import json

# পেজ সেটআপ
st.set_page_config(page_title="AI Audio Translator", layout="centered")
st.title("🎙️ AI Audio Dubber & Language Changer")
st.write("আপনার ভিডিওর অডিও ফাইলটি (MP3/WAV) এখানে আপলোড করুন এবং ডাব করুন!")

# দরকারি ভাষার কোড (ঝামেলাহীন তালিকা)
LANGUAGES = {
    "Bengali": "bn",
    "English": "en",
    "Hindi": "hi",
    "Arabic": "ar",
    "Spanish": "es",
    "French": "fr",
    "Urdu": "ur"
}

# কোনো লাইব্রেরি ছাড়া সরাসরি গুগলের অফিশিয়াল ওয়েব ট্রান্সলেটর ব্যবহার করার ফাংশন
def translate_text(text, target_lang):
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=" + target_lang + "&dt=t&q=" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return "".join([sentence[0] for sentence in data[0]])
    except:
        return text  # সমস্যা হলে মূল লেখা ব্যাকআপ রাখবে

# ইনপুট ইন্টারফেস
uploaded_file = st.file_uploader("আপনার অডিও ফাইলটি আপলোড করুন (MP3/WAV)", type=["mp3", "wav"])
target_lang_name = st.selectbox("কোন ভাষায় ডাব করতে চান?", list(LANGUAGES.keys()))
target_lang_code = LANGUAGES[target_lang_name]

if uploaded_file is not None:
    # ফাইল সেভ করা
    with open("temp_audio.wav", "wb") as f:
        f.write(uploaded_file.read())
    
    st.audio("temp_audio.wav")
    
    if st.button("ডাবিং শুরু করুন 🚀"):
        with st.spinner("এআই আপনার কথাগুলো শুনছে ও অনুবাদ করছে..."):
            try:
                # ১. অডিও থেকে কথা চেনা
                recognizer = sr.Recognizer()
                with sr.AudioFile("temp_audio.wav") as source:
                    audio_data = recognizer.record(source)
                    original_text = recognizer.recognize_google(audio_data)
                
                st.success(f"🗣️ মূল কথা চেনা গেছে: {original_text}")

                # ২. লাইব্রেরি ছাড়া নিরাপদ অনুবাদ
                translated_text = translate_text(original_text, target_lang_code)
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
                
                # ফাইল ডিলিট করে মেমোরি খালি করা
                os.remove("temp_audio.wav")
                os.remove("dubbed_voice.mp3")

            except Exception as e:
                st.error(f"দুঃখিত, কোনো একটি ধাপে সমস্যা হয়েছে। দয়া করে স্পষ্ট কণ্ঠের অডিও ফাইল আপলোড করুন।")
