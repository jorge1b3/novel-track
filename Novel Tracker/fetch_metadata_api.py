import sys
import os
import pathlib
import urllib.request
import urllib.parse
import json
import re
import html
import subprocess

ROOT = pathlib.Path("/home/jorge/Documents/novels/novels")
COVERS_DIR = ROOT / "covers"

def slugify(title):
    s = re.sub(r'[^a-zA-Z0-9 ]', '', title)
    s = s.replace(' ', '_').replace('__', '_').strip('_')
    return s

def clean_html(text):
    if not text:
        return ""
    text = re.sub(r'</p>\s*<p>', ' ', text)
    text = re.sub(r'<p>', '', text)
    text = re.sub(r'</p>', '', text)
    text = re.sub(r'<br\s*/?>', ' ', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Invalid arguments"}))
        sys.exit(1)
        
    url = sys.argv[1].strip()
    title = sys.argv[2].strip()
    
    if not url or 'novelupdates.com/series/' not in url:
        print(json.dumps({"info": "Not a valid NovelUpdates URL, skipping auto-fetch."}))
        sys.exit(0)
        
    slug = slugify(title)
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    
    res_data = {
        "author": "",
        "description": "",
        "genres": [],
        "cover_downloaded": False
    }
    
    try:
        # Fetch NovelUpdates page
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=12) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
        # Scrape Cover URL
        cover_url = ""
        m_img = re.search(r'<div class="seriesimg">\s*<img src="([^"]+)"', html_content)
        if m_img:
            cover_url = m_img.group(1)
            
        # Scrape Description
        m_desc = re.search(r'<div id="editdescription">(.*?)</div>', html_content, re.DOTALL)
        if m_desc:
            res_data["description"] = clean_html(m_desc.group(1))
            
        # Scrape Author
        m_auth = re.search(r'<div id="showauthors">.*?<a[^>]+>(.*?)</a>', html_content, re.DOTALL)
        if m_auth:
            res_data["author"] = html.unescape(m_auth.group(1).strip())
            
        # Scrape Genres
        genres = re.findall(r'href="https://www.novelupdates.com/genre/([^"/]+)/"[^>]*>(.*?)</a>', html_content)
        if genres:
            res_data["genres"] = [html.unescape(g[1].strip()).replace(' ', '_') for g in genres]
            
        # Download and convert cover image
        if cover_url:
            ext = ".jpg"
            if ".png" in cover_url.lower():
                ext = ".png"
            elif ".webp" in cover_url.lower():
                ext = ".webp"
            elif ".jpeg" in cover_url.lower():
                ext = ".jpeg"
                
            temp_path = COVERS_DIR / f"temp_{slug}{ext}"
            webp_path = COVERS_DIR / f"{slug}.webp"
            
            img_req = urllib.request.Request(
                cover_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                temp_path.write_bytes(img_resp.read())
                
            if ext == ".webp":
                if webp_path.exists():
                    webp_path.unlink()
                temp_path.rename(webp_path)
                res_data["cover_downloaded"] = True
            else:
                cmd = ["convert", str(temp_path), str(webp_path)]
                conv_res = subprocess.run(cmd, capture_output=True, text=True)
                if conv_res.returncode == 0 and webp_path.exists() and webp_path.stat().st_size > 0:
                    res_data["cover_downloaded"] = True
                    temp_path.unlink()
                else:
                    # Fallback rename
                    fallback_path = COVERS_DIR / f"{slug}{ext}"
                    if fallback_path.exists():
                        fallback_path.unlink()
                    temp_path.rename(fallback_path)
                    res_data["cover_downloaded"] = True
                    
        print(json.dumps(res_data))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
