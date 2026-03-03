# HookMiner ⛏️

HookMiner is a Python-based automation application designed to scrape viral real estate videos across Instagram and YouTube, filter them by view count, and extract the verbatim spoken "hooks" (the first 10 seconds of dialogue) using Google's Gemini LLM. 

The extracted hooks are exported directly to a CSV, allowing content creators to analyze and identify proven, high-performing video hooks for their own content strategy.

## Features
- **Intelligent Scraping**: Leverages `apify-client` for robust Instagram scraping (bypassing Meta's IP blocks) and `yt-dlp` for YouTube videos.
- **Viral Filtering**: Configurable view count thresholds to only process proven, high-performing videos (e.g., > 1,000,000 views).
- **AI Transcription**: Automatically splices the first 10 seconds of audio via `ffmpeg` and uses Google Gemini 2.5 Flash to transcribe the exact verbal hook.
- **CSV Export**: Aggregates the video URL, creator name, view count, and extracted hook into a clean `proven_hooks.csv` file for easy import into Notion, Excel, or Airtable.

## Prerequisites
- **Python 3.9+**
- **ffmpeg**: Must be installed on your system.
  - macOS: `brew install ffmpeg`
  - Windows/Linux: Download from [ffmpeg.org](https://ffmpeg.org/)

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/HookMiner.git
   cd HookMiner
   ```

2. **Create a virtual environment & install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the script (CLI Mode):**
   If you prefer the terminal, you can still run `python main.py`. It will securely prompt you for your keys and target configuration.
   
## Usage (Local Web Interface)

The easiest and most powerful way to use HookMiner is through its beautiful Local Web Interface.

1. Start the local server:
   ```bash
   python app.py
   ```
2. Open your browser to [http://localhost:5000](http://localhost:5000)
3. Enter your API Keys intuitively into the glassmorphic Configuration Panel.
4. Paste your target social media profiles (one per line).
5. (Optional) Inject specific single video URLs into the "Bypass URLs" field to guarantee their extraction regardless of view count.
6. Click "Start Extraction Pipeline". The terminal on the right side of your screen will stream the real-time Python output!
7. When complete, click the "Download CSV" button to save your `proven_hooks.csv` directly.

## Known Limitations
- Social media platforms routinely update their DOM structures and bot-protection strategies. If `yt-dlp` stops working for a platform, HookMiner falls back to Apify, which is managed by a dedicated scraping community.
- `yt-dlp` utilizes your browser's existing cookies (`cookiesfrombrowser`) to fetch certain content. Ensure that the browser defined in `scanner.py` (default: Chrome) has an active, logged-in session for the targeted platforms if you run into age-restrictions or blockades.

## License
MIT License

# source venv/bin/activate && python app.py