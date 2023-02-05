from fetcher_formatter import *
file_path = "/Users/luil/Desktop/dev/YouTubeAPI/jess_links.txt"

ids_videos = id_extractor(text_link_extractor(file_path))

print(ids_videos)

banned = ["GrFQLYMRJpg" , "ahynBPv58n8"]

for video in ids_videos:
    if video in banned:
        pass
    else:
        transcript, id = transcript_getter(video, ["en"])
        save_subtitles(transcript, id, "txt")