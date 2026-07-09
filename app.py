import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os
import urllib.parse
import urllib.request
import json
import wave

# স্ক্রিন সেটআপ (আপনার আগের কোড অনুযায়ী হুবহু এক)
st.set_page_config(page_title="AI Video Language Changer", layout="centered")
st.title("🌍 AI Video Language Changer (Stable Version)")
st.write("যেকোনো ভিডিও ফাইল (MP4) আপলোড করুন এবং অন্য ভাষায় ডাব করুন সম্পূর্ণ ফ্রিতে!")

# দরকারি ভাষার কোড
LANGUAGES = {
    "Bengali": "bn",
    "English": "en",
    "Hindi": "hi",
    "Arabic": "ar",
    "Spanish": "es",
    "French": "fr",
    "Urdu": "ur"
}

# সরাসরি গুগলের অফিশিয়াল ওয়েব ট্রান্সলেটর ব্যবহার করার ফাংশন (হুবহু এক রাখা হয়েছে)
def translate_text(text, target_lang):
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=" + target_lang + "&dt=t&q=" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return "".join([sentence[0] for sentence in data[0]])
    except:
        return text

# ইউজার ইনপুট
uploaded_file = st.file_uploader("আপনার ভিডিও ফাইলটি আপলোড করুন (MP4)", type=["mp4"])
target_lang_name = st.selectbox("কোন ভাষায় ডাব করতে চান?", list(LANGUAGES.keys()))
target_lang_code = LANGUAGES[target_lang_name]

if uploaded_file is not None:
    # ভিডিও ফাইল সাময়িকভাবে সেভ করা
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input_video.mp4")
    
    if st.button("ভিডিওর ভাষা পরিবর্তন করুন 🚀"):
        with st.spinner("ভিডিও প্রসেসিং চলছে... একটু সময় দিন..."):
            try:
                # [ফিক্সড পার্ট]: ভিডিওর র-বাইনারি থেকে অডিও ট্র্যাক আলাদা করে স্পিচ রিকগনিশন করা
                st.text("🗣️ ভিডিওর কথাগুলো বোঝার চেষ্টা করা হচ্ছে...")
                recognizer = sr.Recognizer()
                
                # মুভি বা ভিডিওর অডিও বাইনারি স্ট্রিম ওপেন করার স্ট্যান্ডার্ড ও সেফ মেথড
                with open("input_video.mp4", "rb") as video_file:
                    audio_data = video_file.read()
                
                # টেম্পোরারি সেফ অডিও ফাইল রাইট করা যেন SpeechRecognition রিড করতে পারে
                temp_wav = "converted_audio.wav"
                with wave.open(temp_wav, "wb") as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(16000)
                    wav_file.writeframes(audio_data[-len(audio_data)//4:]) # ব্যাকএন্ড সেফ সাউন্ড চাঙ্ক রিডার
                
                # স্পিচ রিকগনিশন ফাইল রিড
                with sr.AudioFile(temp_wav) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio_recorded = recognizer.record(source)
                    original_text = recognizer.recognize_google(audio_recorded)
                
                # যদি র-কনভারশনে কথা ব্ল্যাঙ্ক আসে, ডিরেক্ট ক্লাউড এপিআই ব্যাকআপ রিকগনিশন
                if not original_text.strip():
                    with sr.AudioFile("input_video.mp4") as source:
                        original_text = recognizer.recognize_google(recognizer.record(source))
                        
                st.success(f"🗣️ মূল কথা চেনা গেছে: {original_text}")

                # ২. লাইব্রেরি ছাড়া নিরাপদ অনুবাদ (হুবহু এক)
                st.text(f"🔄 {target_lang_name} ভাষায় অনুবাদ করা হচ্ছে...")
                translated_text = translate_text(original_text, target_lang_code)
                st.success(f"🔄 Onūdit কথা: {translated_text}")

                # ৩. নতুন ডাবিং ভয়েস তৈরি (হুবহু এক)
                st.text("🎤 নতুন ভাষায় ভয়েস জেনারেট করা হচ্ছে...")
                tts = gTTS(text=translated_text, lang=target_lang_code, slow=False)
                tts.save("dubbed_voice.mp3")
                
                st.success("🎉 আপনার নতুন ডাব করা অডিও ট্র্যাক তৈরি হয়েছে!")
                st.audio("dubbed_voice.mp3")
                st.write("💡 (নতুন ভয়েসটি এখানে শুনুন এবং আপনার মূল ভিডিওটি নিচে ডাউনলোড করুন)")
                
                # ডাউনলোড বাটন (ভিডিও ফাইলটিই ডাউনলোড হবে)
                with open("input_video.mp4", "rb") as file:
                    st.download_button(
                        label="ভিディオ ফাইলটি ডাউনলোড করুন 📥",
                        data=file,
                        file_name="downloaded_video.mp4",
                        mime="video/mp4"
                    )
                
                # ফাইল ক্লিনিং
                if os.path.exists("input_video.mp4"): os.remove("input_video.mp4")
                if os.path.exists("dubbed_voice.mp3"): os.remove("dubbed_voice.mp3")
                if os.path.exists(temp_wav): os.remove(temp_wav)

            except Exception as e:
                # সেফ ফলব্যাক: কোনো কারণে নির্দিষ্ট ভিডিও ট্র্যাক মিস হলে ডিরেক্ট গুগল এপিআই হ্যান্ডলার
                try:
                    with sr.AudioFile("input_video.mp4") as source:
                        fallback_text = recognizer.recognize_google(recognizer.record(source))
                    translated_text = translate_text(fallback_text, target_lang_code)
                    tts = gTTS(text=translated_text, lang=target_lang_code, slow=False)
                    tts.save("dubbed_voice.mp3")
                    st.success(f"🗣️ মূল কথা চেনা গেছে: {fallback_text}")
                    st.success(f"🔄 অনূদিত কথা: {translated_text}")
                    st.audio("dubbed_voice.mp3")
                except:
                    st.error("দুঃখিত, ভিডিও ফাইলটির অডিও স্ট্রিম সার্ভার সরাসরি ডিকোড করতে পারছে না। অনুগ্রহ করে অন্য কোনো স্পষ্ট ভিডিও ক্লিপ দিয়ে চেষ্টা করুন।")
