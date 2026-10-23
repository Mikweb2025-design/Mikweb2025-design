"""Writes the five newest articles of https://daniele-michelin.com/en/blog/feed.xml between the BLOG markers in README.md."""
import re
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED = "https://daniele-michelin.com/en/blog/feed.xml"
req = urllib.request.Request(FEED, headers={"User-Agent": "github-profile-readme"})
root = ET.fromstring(urllib.request.urlopen(req, timeout=20).read())
lines = []
for item in root.iter("item"):
    title, link, date = item.findtext("title"), item.findtext("link"), item.findtext("pubDate")
    lines.append(f"- [{title}]({link}) · {parsedate_to_datetime(date):%Y-%m-%d}")
    if len(lines) == 5:
        break
readme = open("README.md", encoding="utf-8").read()
block = "<!-- BLOG:START -->\n" + "\n".join(lines) + "\n<!-- BLOG:END -->"
new = re.sub(r"<!-- BLOG:START -->.*?<!-- BLOG:END -->", lambda m: block, readme, flags=re.S)
if new != readme:
    open("README.md", "w", encoding="utf-8").write(new)
    print("updated")
