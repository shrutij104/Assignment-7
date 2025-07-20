
import requests
import re

API_KEY = "AIzaSyDMb8oU8a2kLoDsfdxCqaXpUEe33UmbARw"
API_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + API_KEY

def extract_urls(text):
    """Extract URLs from email text using regex."""
    url_pattern = r"https?://[^\s]+"
    return re.findall(url_pattern, text)

def check_phishing(url):
    """Check if a URL is malicious using Google Safe Browsing API."""
    payload = {
        "client": {"clientId": "spam-detector", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200 and "matches" in response.json():
        return "⚠️ Phishing Link Detected!"
    return "✅ Safe Link"

