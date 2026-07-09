import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os
import urllib.parse
import urllib.request
import json
import av

# স্ক্রিন সেটআপ (আপনার আগের ডিজাইন অনুযায়ী হুবহু এক)
st.set_page_config(page_title="AI Video Language Changer", layout="centered")
st.title("🌍 AI Video Language Changer (Stable Version)")
st.write("যেকোনো ভিডিও ফাইল (MP4) আপলোড করুন এবং অন্য ভাষায় ডাব করুন সম্পূর্ণ ফ্রিতে!")

# দরকারি ভাষার কোড (হুবহু এক)
LANGUAGES = {
    "Bengali": "bn",
    "English": "en",
    "Hindi": "hi",
    "Arabic": "ar",
    "Spanish": "es",
    "French": "fr",
    "Urdu": "ur"
}

# সরাসরি গুগলের অফিশিয়াল ওয়েব ট্রান্সলেটর ব্যবহার করার ফাংশন (হুবহু এক)
def translate_text(text, target_lang):
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=" + target_lang + "&dt=t&q=" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return "".join([sentence[0] for sentence in data[0]])
    except:
        return text

# ইউজার ইনপুট (হুবহু এক)
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
                st.text("🗣️ ভিডিওর কথাগুলো বোঝার চেষ্টা করা হচ্ছে...")
                
                # 'av' লাইব্রেরি দিয়ে ভিডিও থেকে অডিও কন্টেইনার আলাদা করা
                container = av.open("input_video.mp4")
                stream = container.streams.audio[0]
                
                # র-অডিও ডাটা কনভার্ট করে সেভ করা
                with open("extracted_audio.wav", "wb") as f_audio:
                    for packet in container.demux(stream):
                        for frame in packet.decode():
                            # অডিও ফ্রেম রাইট করা
                            f_audio.write(frame.to_ndarray().tobytes())
                container.close()
                
                # স্পিচ রিকগনিশন
                recognizer = sr.Recognizer()
                with sr.AudioFile("extracted_audio.wav") as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio_recorded = recognizer.record(source)
                    original_text = recognizer.recognize_google(audio_recorded)
                
                st.success(f"🗣️ মূল কথা চেনা গেছে: {original_text}")

                # ২. লাইব্রেরি ছাড়া নিরাপদ অনুবাদ (হুবহু এক)
                st.text(f"🔄 {target_lang_name} ভাষায় অনুবাদ করা হচ্ছে...")
                translated_text = translate_text(original_text, target_lang_code)
                st.success(f"🔄 অনূদিত কথা: {translated_text}")

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
                        label="ভিডিও ফাইলটি ডাউনলোড করুন 📥",
                        data=file,
                        file_name="downloaded_video.mp4",
                        mime="video/mp4"
                    )
                
                # ফাইল ক্লিনিং
                if os.path.exists("input_video.mp4"): os.remove("input_video.mp4")
                if os.path.exists("extracted_audio.wav"): os.remove("extracted_audio.wav")
                if os.path.exists("dubbed_voice.mp3"): os.remove("dubbed_voice.mp3")

            except Exception as e:
                st.error(f"দুঃখিত, ভিডিও ফাইলটি প্রসেস করতে সমস্যা হয়েছে। এরর বিবরণ: {str(e)}")
