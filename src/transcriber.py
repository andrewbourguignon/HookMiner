import os
import subprocess
import yt_dlp
from google import genai

def transcribe_video(video):
    """
    Pulls the first 10 seconds of audio and converts it to text.
    Extracts the verbatim hook using an LLM (Gemini API).
    Returns the hook text.
    """
    url = video.get('url')
    if not url:
        return None
        
    print(f"Processing transcript for: {url}")
    
    # Setup temp directory
    os.makedirs('temp', exist_ok=True)
    raw_audio_path = f"temp/raw_{video.get('id', 'audio')}.m4a"
    trimmed_audio_path = f"temp/trimmed_{video.get('id', 'audio')}.m4a"
    
    # 1. Download audio
    # If Apify gave us a direct MP4 URL, use urllib to download it quickly. 
    # Otherwise, fallback to yt-dlp which sometimes still handles direct post URLs.
    direct_mp4 = video.get('video_url')
    
    try:
        if direct_mp4:
            import urllib.request
            urllib.request.urlretrieve(direct_mp4, raw_audio_path)
        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': raw_audio_path,
                'quiet': True,
                'ignoreerrors': True,
                'cookiesfrombrowser': ('chrome',), 
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
        if not os.path.exists(raw_audio_path):
            print("Failed to download audio.")
            return None
            
        # 2. Trim audio using ffmpeg
        subprocess.run([
            'ffmpeg', '-y', '-i', raw_audio_path, 
            '-ss', '00:00:00', '-t', '00:00:10', 
            '-c', 'copy', trimmed_audio_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # 3. Use Gemini to extract the hook
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY environment variable not set.")
            return None
            
        # Initialize the modern GenAI client
        client = genai.Client(api_key=api_key)
        
        # Upload the file using the modern API
        print("Uploading to Gemini...")
        audio_file = client.files.upload(file=trimmed_audio_path)
        
        # Generate content
        prompt = "Listen to the first 10 seconds of this audio and transcribe the verbatim words spoken. This is meant to be a social media 'hook'. Just output the exact words spoken, no other text or commentary."
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, audio_file]
        )
        
        hook = response.text.strip()
        print(f"Extracted Hook: {hook}")
        
    except Exception as e:
        print(f"Transcription error: {e}")
        hook = None
    finally:
        # Cleanup temp files
        if os.path.exists(raw_audio_path):
            os.remove(raw_audio_path)
        if os.path.exists(trimmed_audio_path):
            os.remove(trimmed_audio_path)
            
    return hook

