"""
HookMiner - Viral Real Estate Video Scraper & Hook Extractor
"""
import os
import getpass
from src.scanner import scan_handles
from src.filter import filter_videos
from src.transcriber import transcribe_video
from src.generator import export_to_csv

# Add the specific Instagram or TikTok handles here
TARGET_HANDLES = [
    "https://www.instagram.com/instagram/", # Generic example, replace with your targets
    "https://www.youtube.com/@youtube",
]

# The minimum number of views a video needs to be transcribed
MIN_VIEWS = 1000000

def main():
    print("Starting HookMiner execution...")
    
    if not os.getenv("APIFY_API_TOKEN"):
        os.environ["APIFY_API_TOKEN"] = getpass.getpass("\nEnter your Apify API Token (input hidden): ")
        
    if not os.getenv("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = getpass.getpass("Enter your Gemini API Key (input hidden): ")
        
    print(f"Target handles: {TARGET_HANDLES}")
    
    # 1. Scan handles (limit to Top 10 recent videos each for speed)
    print("\n--- PHASE 1: SCANNING HANDLES ---")
    videos = scan_handles(TARGET_HANDLES, max_videos_per_handle=10)
    print(f"Total videos scanned: {len(videos)}")
    
    if not videos:
        print("No videos found. Exiting.")
        return

    # 2. Filter videos
    print(f"\n--- PHASE 2: FILTERING VIRAL VIDEOS (>={MIN_VIEWS} Views) ---")
    viral_videos = filter_videos(videos, min_views=MIN_VIEWS)
    
    if not viral_videos:
        print("No viral videos found matching the criteria. Exiting.")
        return
        
    # 3. Transcribe and extract hooks
    print("\n--- PHASE 3: EXTRACTING HOOKS VIA GEMINI AI ---")
    hooks_data = []
    
    # Limit number of transcriptions processed to save API calls during development (e.g. first 5)
    MAX_TO_PROCESS = 5 
    print(f"Processing up to {MAX_TO_PROCESS} viral videos...")
    
    for count, video in enumerate(viral_videos):
        if count >= MAX_TO_PROCESS:
            break
            
        print(f"[{count+1}/{len(viral_videos)}] Processing: {video.get('title')}")
        hook_text = transcribe_video(video)
        
        if hook_text:
            # We construct a final flat dictionary to easily export to CSV
            row = {
                'creator': video.get('creator'),
                'title': video.get('title'),
                'url': video.get('url'),
                'views': video.get('views'),
                'duration': video.get('duration'),
                'hook': hook_text
            }
            hooks_data.append(row)
            
    # 4. Generate CSV
    print("\n--- PHASE 4: EXPORTING DATA ---")
    if hooks_data:
        export_to_csv(hooks_data, filename="proven_hooks.csv")
    else:
        print("No hooks extracted. Nothing to export.")
        
    print("\nHookMiner execution completed.")

if __name__ == "__main__":
    main()

