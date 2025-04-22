# Bengali Voice Weather Assistant

A voice-enabled weather assistant that provides weather information in Bengali language through both voice and text interfaces.

## Features

- Voice and text input support
- Bengali language interface
- Real-time weather information
- Text-to-speech output in Bengali
- Support for 8 major cities in Bangladesh
- Interactive Streamlit web interface

## Requirements

- Python 3.7+
- Required Python packages (listed in requirements.txt)
- Working microphone for voice input
- Internet connection
- OpenWeatherMap API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/voice_assistant.git
cd voice_assistant
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Configure API Key:
   - Create a `.streamlit/secrets.toml` file
   - Add your OpenWeatherMap API key:
   ```toml
   weather_api_key = "your_api_key_here"
   ```

## Usage

1. Start the application:
```bash
streamlit run streamlit_weather_app.py
```

2. Using Voice Input:
   - Click on the "Voice" tab
   - Press the "কথা বলুন" (Speak) button
   - Say "আবহাওয়া" (weather) followed by your query
   - Listen to the response

3. Using Text Input:
   - Click on the "Text" tab
   - Type your query including the word "আবহাওয়া"
   - Click "জানতে চাই" (Submit) button
   - Read or listen to the response

## Supported Cities

- ঢাকা (Dhaka)
- চট্টগ্রাম (Chittagong)
- খুলনা (Khulna)
- রাজশাহী (Rajshahi)
- সিলেট (Sylhet)
- বরিশাল (Barisal)
- রংপুর (Rangpur)
- ময়মনসিংহ (Mymensingh)

## Developer

Created by: Shafin Tamim
