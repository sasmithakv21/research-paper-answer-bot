import os
import requests
from pathlib import Path

PAPERS_DIR = Path(__file__).parent / "data" / "papers"
PAPERS_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_PAPERS = {
    "attention_is_all_you_need.pdf": "https://arxiv.org/pdf/1706.03762.pdf",
    "resnet_deep_learning.pdf": "https://arxiv.org/pdf/1512.03385.pdf"
}

def download_papers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    for filename, url in SAMPLE_PAPERS.items():
        filepath = PAPERS_DIR / filename
        # Remove empty files if any
        if filepath.exists() and filepath.stat().st_size == 0:
            filepath.unlink()

        if not filepath.exists():
            print(f"Downloading {filename} from {url}...")
            try:
                response = requests.get(url, headers=headers, timeout=30)
                if response.status_code == 200:
                    with open(filepath, 'wb') as out_file:
                        out_file.write(response.content)
                    print(f"Successfully saved {filename} ({filepath.stat().st_size} bytes)")
                else:
                    print(f"Failed to download {filename}: HTTP {response.status_code}")
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
        else:
            print(f"Paper {filename} already exists at {filepath} ({filepath.stat().st_size} bytes)")

if __name__ == "__main__":
    download_papers()
