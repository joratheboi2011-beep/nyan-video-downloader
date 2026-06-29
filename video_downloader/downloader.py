import os
import re
import requests
import yt_dlp

def download_direct_url(url, output_dir="downloads"):
    """Downloads direct file links like Discord CDN."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Extract filename from URL or use a default
    filename = url.split('/')[-1].split('?')[0]
    if not filename.endswith(('.mp4', '.mkv', '.webm', '.mov')):
        filename += ".mp4"
        
    output_path = os.path.join(output_dir, filename)
    print(f"[*] Downloading direct link to {output_path}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"[+] Download complete: {output_path}")

def download_via_ytdlp(url, output_dir="downloads"):
    """Downloads videos using yt-dlp (YouTube, TikTok, Douyin)."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': True,
    }
    
    print(f"[*] Extracting and downloading via yt-dlp: {url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    url = input("Enter the video URL (YouTube, TikTok, Douyin, or Discord): ").strip()
    
    if not url:
        print("[-] URL cannot be empty.")
        return

    # Check if it is a direct Discord CDN asset link
    if "discordapp.net" in url or "discordapp.com" in url:
        try:
            download_direct_url(url)
        except Exception as e:
            print(f"[-] Failed to download Discord asset: {e}")
    # Fallback to yt-dlp for YouTube, TikTok, and Douyin
    else:
        try:
            download_via_ytdlp(url)
        except Exception as e:
            print(f"[-] Failed to download via yt-dlp: {e}")

if __name__ == "__main__":
    main()
