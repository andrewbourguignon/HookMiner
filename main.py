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
    "https://www.instagram.com/ryanserhant/",
]

# Add specific individual video URLs here that you want to force-process
# These videos will bypass the MIN_VIEWS filter and always be transcribed
TARGET_VIDEOS = [
    "https://www.youtube.com/watch?v=0w12sXqA-wE",
]

# The minimum number of views a video needs to be transcribed
MIN_VIEWS = 1000000

# The maximum number of videos to scan per profile
SCAN_LIMIT = 10

def run_pipeline(apify_token, gemini_key, target_handles, target_videos, min_views, scan_limit):
    print("Starting HookMiner execution...")
    
    os.environ["APIFY_API_TOKEN"] = apify_token
    os.environ["GEMINI_API_KEY"] = gemini_key
        
    print(f"Target handles: {target_handles}")
    if target_videos:
        print(f"Target videos: {target_videos}")
    
    # 1. Scan handles (limit to Top 10 recent videos each for speed)
    print("\n--- PHASE 1: SCANNING HANDLES ---")
    videos = []
    if target_handles:
        videos = scan_handles(target_handles, max_videos_per_handle=scan_limit)
        print(f"Total videos scanned: {len(videos)}")
    
    # 2. Filter videos
    viral_videos = []
    if videos:
        print(f"\n--- PHASE 2: FILTERING VIRAL VIDEOS (>={min_views} Views) ---")
        viral_videos = filter_videos(videos, min_views=min_views)
    
    # 2b. Add the forced TARGET_VIDEOS that bypass the filter
    if target_videos:
        print(f"\n--- PHASE 2b: INJECTING {len(target_videos)} SPECIFIC TARGET VIDEOS ---")
        # We can re-use the scanner logic on specific URLs, which will fetch their metadata
        specific_videos = scan_handles(target_videos, max_videos_per_handle=1)
        viral_videos.extend(specific_videos)
        
    if not viral_videos:
        print("No videos found matching the criteria. Exiting.")
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
        print("Successfully exported hooks to data/proven_hooks.csv")
    else:
        print("No hooks extracted. Nothing to export.")
        
    print("\nHookMiner execution completed.")

def main():
    # CLI Mode compatibility
    apify_token = os.getenv("APIFY_API_TOKEN")
    if not apify_token:
        apify_token = getpass.getpass("\nEnter your Apify API Token (input hidden): ")
        
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        gemini_key = getpass.getpass("Enter your Gemini API Key (input hidden): ")
        
    run_pipeline(apify_token, gemini_key, TARGET_HANDLES, TARGET_VIDEOS, MIN_VIEWS, SCAN_LIMIT)

if __name__ == "__main__":
    main()

