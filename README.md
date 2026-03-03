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

3. **Run the script:**
   The script will securely prompt you for your API keys when run, ensuring they are never saved in any project files.
   - **GEMINI_API_KEY**: Get a free key from [Google AI Studio](https://aistudio.google.com/).
   - **APIFY_API_TOKEN**: Create a free account at [Apify](https://apify.com) and get your personal API token.

## Usage

1. Open `main.py` in your preferred code editor.
2. Edit the `TARGET_HANDLES` array with the URLs of the specific Instagram or YouTube profiles you want to mine for hooks.
3. (Optional) Adjust the `MIN_VIEWS` threshold (default is 1,000,000).
4. Run the script:
   ```bash
   python main.py
   ```

The script will ask for your keys and begin mining. It will output a `proven_hooks.csv` file inside a newly created `/data` directory.

## Known Limitations
- Social media platforms routinely update their DOM structures and bot-protection strategies. If `yt-dlp` stops working for a platform, HookMiner falls back to Apify, which is managed by a dedicated scraping community.
- `yt-dlp` utilizes your browser's existing cookies (`cookiesfrombrowser`) to fetch certain content. Ensure that the browser defined in `scanner.py` (default: Chrome) has an active, logged-in session for the targeted platforms if you run into age-restrictions or blockades.

## License
MIT License
