import sys
import os
import pathlib
import urllib.request
import urllib.parse
import subprocess
import re

ROOT = pathlib.Path("/home/jorge/Documents/novels/novels")
COVERS_DIR = ROOT / "covers"

def slugify(title):
    s = re.sub(r'[^a-zA-Z0-9 ]', '', title)
    s = s.replace(' ', '_').replace('__', '_').strip('_')
    return s

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 download_cover.py <url> <title>")
        sys.exit(1)
        
    url = sys.argv[1].strip()
    title = sys.argv[2].strip()
    
    if not url:
        print("Empty URL, skipping cover download.")
        sys.exit(0)
        
    if not title:
        print("Empty title, cannot determine target filename.")
        sys.exit(1)
        
    slug = slugify(title)
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Extract file extension from URL if possible, otherwise default to .jpg
    ext = ".jpg"
    try:
        parsed_url = urllib.parse.urlparse(url)
        path_suffix = os.path.splitext(parsed_url.path)[1].lower()
        if path_suffix in [".jpg", ".jpeg", ".png", ".webp"]:
            ext = path_suffix
    except Exception:
        pass
        
    temp_file = COVERS_DIR / f"temp_{slug}{ext}"
    out_webp_path = COVERS_DIR / f"{slug}.webp"
    
    print(f"Downloading cover from {url}...")
    try:
        # Use a user agent header to prevent HTTP 403 Forbidden errors
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=20) as response:
            with open(temp_file, 'wb') as out_file:
                out_file.write(response.read())
        
        print("Download finished. Converting to WebP...")
        
        # If it is already a webp, we can just rename it. Otherwise convert it.
        if ext == ".webp":
            if out_webp_path.exists():
                out_webp_path.unlink()
            temp_file.rename(out_webp_path)
            print(f"Saved: covers/{slug}.webp")
        else:
            cmd = ["convert", str(temp_file), str(out_webp_path)]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0 and out_webp_path.exists() and out_webp_path.stat().st_size > 0:
                print(f"Converted and saved: covers/{slug}.webp")
                if temp_file.exists():
                    temp_file.unlink()
            else:
                # If ImageMagick convert fails, try standard save as fallback
                print(f"Convert failed: {res.stderr}. Saving original format as fallback...")
                fallback_path = COVERS_DIR / f"{slug}{ext}"
                if fallback_path.exists():
                    fallback_path.unlink()
                temp_file.rename(fallback_path)
                print(f"Saved fallback: covers/{slug}{ext}")
    except Exception as e:
        print(f"Error downloading or converting cover: {e}")
        if temp_file.exists():
            temp_file.unlink()
        sys.exit(1)

if __name__ == "__main__":
    main()
