from pathlib import Path
import json

# Construct the YouTube links with the Video_ids
video_ids_path = Path("video_ids.json")

with video_ids_path.open(mode="r") as file:
    video_ids = json.load(file)

youtube_links = []
for i in video_ids:
    youtube_link = f"https://www.youtube.com/watch?v={i}"
    youtube_links.append(youtube_link)

all_links = Path("youtube_links.json")
with all_links.open(mode="w") as file:
    json.dump(youtube_links, file, indent=4)





