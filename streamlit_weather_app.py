import streamlit as st
import speech_recognition as sr
from gtts import gTTS  # Changed from 'gTTS import gTTS'
import requests
import io
import time

class StreamlitWeatherAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000  # Adjust microphone sensitivity
        self.recognizer.dynamic_energy_threshold = True
        self.weather_api_key = st.secrets["weather_api_key"]
        self.city = "Dhaka"
        self.weather_keywords = ["আবহাওয়া", "তাপমাত্রা", "বাতাস", "weather"]
        self.cities = {
            "ঢাকা": "Dhaka",
            "চট্টগ্রাম": "Chittagong",
            "খুলনা": "Khulna",
            "রাজশাহী": "Rajshahi",
            "সিলেট": "Sylhet",
            "বরিশাল": "Barisal",
            "রংপুর": "Rangpur",
            "ময়মনসিংহ": "Mymensingh"
        }

    def contains_weather_keywords(self, text):
        return any(keyword in text.lower() for keyword in self.weather_keywords)

    def get_weather(self):
        try:
            # Correct API endpoint
            url = (
                "https://api.openweathermap.org/data/2.5/weather"
                f"?q={self.city}"
                f"&appid={self.weather_api_key.strip()}"
                "&units=metric"
            )
            
            # Print debug info before request
            print(f"Requesting URL: {url}")
            
            response = requests.get(url, timeout=10)
            
            try:
                data = response.json()
                print(f"Status Code: {response.status_code}")
                print(f"Response: {data}")
            except ValueError as e:
                print(f"JSON Decode Error: {e}")
                return False, "ডেটা পার্স করতে সমস্যা হয়েছে"
            
            if response.status_code == 200:
                temp = round(data['main']['temp'])
                humidity = data['main']['humidity']
                feels_like = round(data['main']['feels_like'])
                
                weather_text = (
                    f"বর্তমান তাপমাত্রা {temp} ডিগ্রি সেলসিয়াস।\n"
                    f"অনুভূত তাপমাত্রা {feels_like} ডিগ্রি সেলসিয়াস।\n"
                    f"আর্দ্রতা {humidity} শতাংশ।"
                )
                return True, weather_text
            elif response.status_code == 401:
                return False, "API কী সমস্যা। কী চেক করুন।"
            elif response.status_code == 404:
                return False, "শহরের নাম পাওয়া যায়নি"
            else:
                return False, f"সার্ভার ত্রুটি: {response.status_code}"
                
        except requests.Timeout:
            return False, "সার্ভার রেসপন্স টাইম আউট"
        except requests.ConnectionError:
            return False, "ইন্টারনেট সংযোগ নেই"
        except Exception as e:
            print(f"Error details: {str(e)}")
            return False, "অপ্রত্যাশিত সমস্যা দেখা দিয়েছে"

    def text_to_speech(self, text):
        try:
            tts = gTTS(text=text, lang='bn', slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return True, audio_buffer
        except Exception as e:
            return False, f"Error in speech synthesis: {str(e)}"

    def listen_for_speech(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
                return True, audio
            except sr.WaitTimeoutError:
                return False, "সময়সীমা শেষ, আবার চেষ্টা করুন"
            except Exception as e:
                return False, str(e)

def initialize_session_state():
    if 'recording' not in st.session_state:
        st.session_state.recording = False
    if 'last_query' not in st.session_state:
        st.session_state.last_query = None
    if 'weather_info' not in st.session_state:
        st.session_state.weather_info = None

def main():
    st.set_page_config(
        page_title="বাংলা আবহাওয়া সহকারী",
        page_icon="🌤️",
        layout="centered"
    )
    
    initialize_session_state()
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 1rem;
        }
        .stButton>button {
            width: 100%;
            margin: 0.5rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("বাংলা আবহাওয়া সহকারী 🌤️")
    
    assistant = StreamlitWeatherAssistant()

    # Main layout without city selection
    with st.expander("ব্যবহার নির্দেশিকা ℹ️"):
        selected_city = st.selectbox(
            "শহর",
            options=list(assistant.cities.keys()),
            format_func=lambda x: x
        )
        assistant.city = assistant.cities[selected_city]
        st.markdown("1. কথা বলুন অথবা টেক্সট লিখুন")
        st.markdown("2. আবহাওয়ার তথ্য জানতে 'আবহাওয়া' শব্দটি ব্যবহার করুন")

    # Main content
    tab1, tab2 = st.tabs(["🎤 ভয়েস", "⌨️ টেক্সট"])
    
    with tab1:
        st.markdown("##### কথা বলে আবহাওয়া জানুন")
        if st.button("🎙️ কথা বলুন", key="voice_button"):
            with st.spinner("শুনছি..."):
                try:
                    st.session_state.recording = True
                    success, result = assistant.listen_for_speech()
                    
                    if not success:
                        st.error(result)
                        return
                        
                    audio = result
                    with st.spinner("প্রক্রিয়াকরণ হচ্ছে..."):
                        text = assistant.recognizer.recognize_google(audio, language='bn-BD')
                        st.session_state.last_query = text
                        
                        if assistant.contains_weather_keywords(text):
                            success, weather_info = assistant.get_weather()
                            if success:
                                st.success(f"আপনার প্রশ্ন: {text}")
                                st.write(weather_info)
                                success, audio_buffer = assistant.text_to_speech(weather_info)
                                if success:
                                    st.audio(audio_buffer, format='audio/mp3', start_time=0)
                            else:
                                st.error(weather_info)
                        else:
                            st.warning("আবহাওয়া সম্পর্কে জিজ্ঞাসা করুন")
                            
                except sr.UnknownValueError:
                    st.warning("কিছু শুনতে পাইনি, আবার চেষ্টা করুন")
                except sr.RequestError:
                    st.error("নেটওয়ার্ক সমস্যা, আবার চেষ্টা করুন")
                except Exception as e:
                    st.error(f"সমস্যা হয়েছে: {str(e)}")
                finally:
                    st.session_state.recording = False

    with tab2:
        st.markdown("##### টেক্সট লিখে আবহাওয়া জানুন")
        query = st.text_input("আপনার প্রশ্ন লিখুন", placeholder="আবহাওয়া কেমন?", key="text_input")
        
        if st.button("জানতে চাই", key="text_button") and query:
            if assistant.contains_weather_keywords(query):
                success, weather_info = assistant.get_weather()
                if success:
                    st.write(weather_info)
                    success, audio_buffer = assistant.text_to_speech(weather_info)
                    if success:
                        st.audio(audio_buffer, format='audio/mp3')
                else:
                    st.error(weather_info)
            else:
                st.warning("আবহাওয়া সম্পর্কে জিজ্ঞাসা করুন")

    # Footer
    st.markdown("---")
    st.markdown("### তৈরি করেছে: Shafin Tamim")

if __name__ == "__main__":
    main()
