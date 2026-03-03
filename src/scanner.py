import os
from apify_client import ApifyClient

def scan_handles(handles, max_videos_per_handle=10):
    """
    Scans a list of specific social media handles using Apify API.
    Fetches video metadata (Views, Creator, URL).
    Returns a list of video dictionaries.
    """
    api_key = os.getenv("APIFY_API_TOKEN")
    if not api_key:
        print("Error: APIFY_API_TOKEN environment variable not set.")
        return []
        
    client = ApifyClient(api_key)
    all_videos = []
    
    # Process Instagram handles vs others (Apify has specific scrapers for each platform)
    instagram_handles = [h for h in handles if 'instagram.com' in h]
    youtube_handles = [h for h in handles if 'youtube.com' in h]
    
    if instagram_handles:
        print(f"Scanning {len(instagram_handles)} Instagram handles via Apify...")
        
        # We use a popular, reliable actor for Instagram Profiles
        run_input = {
            "addParentData": False,
            "directUrls": instagram_handles,
            "enhanceUserSearchWithFacebookPage": False,
            "isUserReelFeedURL": False,
            "isUserTaggedFeedURL": False,
            "resultsLimit": max_videos_per_handle,
            "resultsType": "posts",
            "searchLimit": 1,
            "searchType": "hashtag"
        }

        try:
            # Run the apify/instagram-scraper actor
            actor_call = client.actor("apify/instagram-scraper").call(run_input=run_input)
            
            # Fetch results from the dataset
            dataset_items = client.dataset(actor_call["defaultDatasetId"]).iterate_items()
            
            for item in dataset_items:
                # Instagram scraper might return image posts, we only want video/reels
                if item.get("videoUrl"):
                    video_data = {
                        'url': item.get("url"), # The post URL
                        'video_url': item.get("videoUrl"), # The direct MP4 link
                        'creator': item.get("ownerUsername", "Unknown"),
                        'title': item.get("caption", "No Caption")[:100] if item.get("caption") else "No Caption", # Trucate long captions
                        'views': item.get("videoPlayCount", 0),
                        'duration': item.get("videoDuration", 0)
                    }
                    all_videos.append(video_data)
        except Exception as e:
            print(f"Apify Instagram scraping failed: {e}")
            
    # For other platforms like YouTube and Facebook, use yt-dlp natively
    other_handles = [h for h in handles if 'instagram.com' not in h]
    
    if other_handles:
        print(f"Scanning {len(other_handles)} other handles (YouTube/Facebook) natively with yt-dlp...")
        import yt_dlp
        
        ydl_opts = {
            'extract_flat': 'in_playlist',
            'playlistend': max_videos_per_handle,
            'quiet': True,
            'ignoreerrors': True,
            'cookiesfrombrowser': ('chrome',), 
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for handle in other_handles:
                print(f"Scanning yt-dlp handle: {handle}")
                try:
                    info = ydl.extract_info(handle, download=False)
                    if not info:
                        continue
                        
                    entries = info.get('entries', [info])
                    
                    for entry in entries:
                        if entry:
                            video_data = {
                                'url': entry.get('url') or entry.get('webpage_url'),
                                'creator': entry.get('uploader') or entry.get('channel') or handle,
                                'title': entry.get('title', 'Unknown Title'),
                                'views': entry.get('view_count', 0),
                                'duration': entry.get('duration', 0)
                            }
                            if video_data['url']:
                                all_videos.append(video_data)
                except Exception as e:
                    print(f"Error scanning {handle} with yt-dlp: {e}")

    return all_videos

