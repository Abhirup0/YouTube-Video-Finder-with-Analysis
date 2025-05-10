# 🎬 YouTube Video Finder with Analysis

<div align="center">

![YouTube Video Finder Banner](https://img.shields.io/badge/YouTube%20Video%20Finder-AI%20Powered-red?style=for-the-badge&logo=youtube)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![YouTube API](https://img.shields.io/badge/YouTube%20Data-API%20v3-red.svg?logo=youtube)](https://developers.google.com/youtube/v3)
[![Gemini API](https://img.shields.io/badge/Google-Gemini%20API-blue.svg?logo=google&logoColor=white)](https://ai.google.dev/gemini-api)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

*A smart CLI tool that finds the best YouTube videos based on your query using AI analysis*

</div>

## ✨ Features

<div align="center">
  <img src="https://raw.githubusercontent.com/Abhirup0/YouTube-Video-Finder-with-Analysis/main/docs/screenshot.png" alt="YouTube Video Finder Screenshot" width="700">
</div>

- 🗣️ **Multiple Input Methods**: Accept voice or text input (supports both Hindi and English)
- 🔍 **Smart Search**: Find relevant YouTube videos based on your query
- ⏱️ **Intelligent Filtering**:
  - Videos between 4-20 minutes in length
  - Only videos published in the last 14 days
  - Returns the top 20 results
- 🧠 **AI-Powered Analysis**: Uses Google's Gemini 1.5 Flash to analyze video titles
- 🏆 **Best Recommendation**: Suggests the most relevant video with an explanation
- 💻 **Beautiful CLI Interface**: Colorful and user-friendly terminal interface

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- YouTube Data API v3 key ([Get one here](https://console.cloud.google.com/apis/library/youtube.googleapis.com))
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/Abhirup0/YouTube-Video-Finder-with-Analysis.git
   cd YouTube-Video-Finder-with-Analysis
   ```

2. **Install the required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate the config file**
   ```bash
   python run.py
   ```

4. **Add your API keys**
   
   Edit the generated `config/config.json` file:
   ```json
   {
       "youtube_api_key": "YOUR_YOUTUBE_API_KEY",
       "gemini_api_key": "YOUR_GEMINI_API_KEY"
   }
   ```

### Usage

Run the main script:
```bash
python run.py
```

<div align="center">
  <img src="https://raw.githubusercontent.com/Abhirup0/YouTube-Video-Finder-with-Analysis/main/docs/workflow.gif" alt="Application Workflow" width="600">
</div>

Follow the prompts to:
1. Choose input method (text or voice)
2. Enter your search query
3. View the results and recommendation

## 🎙️ Voice Input Requirements

For voice input to work:
- SpeechRecognition package must be installed
- PyAudio package must be installed
- Active microphone connection

```bash
# On Windows (if PyAudio installation fails)
pip install pipwin
pipwin install pyaudio

# On Linux
sudo apt-get install portaudio19-dev python-pyaudio
pip install pyaudio
```

## 📋 Project Structure

```
youtube_finder/
├── config/
│   └── config.json         # API keys configuration
├── src/
│   ├── config_manager.py   # Configuration loading/saving
│   ├── llm_analysis.py     # Gemini API integration
│   ├── main.py             # Main application script
│   ├── test.py             # Test suite
│   ├── text_input.py       # Text/voice input handling
│   └── youtube_search.py   # YouTube API integration
├── README.md               # This file
├── requirements.txt        # Python dependencies
└── run.py                  # Entry point script
```

## 📝 Notes

- Voice input quality depends on microphone quality and ambient noise
- API rate limits may apply based on your key tier
- The application is designed to work in a command-line interface

## 🔮 Future Improvements

- [ ] Add a web interface
- [ ] Include more filtering options (channel, category, etc.)
- [ ] Implement video content analysis (not just titles)
- [ ] Support for more languages
- [ ] Add offline mode using cached results

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [YouTube Data API v3](https://developers.google.com/youtube/v3)
- Powered by [Google Gemini API](https://ai.google.dev/)
- Special thanks to all the open-source libraries used in this project 