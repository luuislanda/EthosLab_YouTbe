from youtube_transcript_api import YouTubeTranscriptApi
import youtube_transcript_api.formatters as formatter 
from urlextract import URLExtract 
import yt_dlp
import zipfile
import urllib.request
import json
import re

# Cookies are required for certain videos such as age-restricted videos, this means they may have to be re-purposed
# Need to create exceptions for deleted/private videos... these should be notified as unavailable but not stop the script

hard_file_path = "/Users/luil/Desktop/dev/YouTubeAPI/jess_links.txt" #currently hardcoded to avoid 

#TODO: either make function or modify app file to make sure file path is specificed by user in CLI and uploaded in the webapp
#TODO: find a way to download things chronologically
#TODO: digital caption trail
#TODO: allow user to download subtitles in zip format


def text_link_extractor(file_path: str) -> list[str]:
   
    '''Extract the URLs from any text or reference page, currently only accepts files as input
    It outputs a list where each item is a string '''
    
    links = []
    extractor = URLExtract()
    with open(file_path, "r") as myfile:
        for line in myfile.readlines():
            urls = extractor.find_urls(line)
            if len(urls) != 0:
                links.append(urls)
    
    return links       


def playlist_link_extractor(playlist_url: str) -> list[str]:
    '''
    Given a playlist URL, this function creates a list of all the YouTube video links
    '''
    videos = yt_dlp.PlaylistEntries(playlist_url)

    # Extract the links from the list of videos
    playlist_links = [video['webpage_url'] for video in videos]

    return playlist_links  



def id_extractor(urls: list) -> list[str]:
     
    '''Looks for *YouTube* URLs in strings and extracts the Video ID.
    It accounts for some of the variations and shortlinks, but may need updating'''
   
    ids = []
    #Video IDs tend to be 11 characters, case-insensitive
    pattern = r'(?:https?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtube|youtu|youtube-nocookie)\.(?:com|be)\/(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})'
    for url in urls:
        ids.append(re.findall(pattern, url, re.MULTILINE | re.IGNORECASE))
    ids = [item for sublist in ids for item in sublist] #flattens list

    return ids

def transcript_getter(video_id: str, languages= ["en"]):
    
    '''This function fetches transcripts based on the languages specified by the user
    By default, it tries to first obtain those that are manually created. However if it doesnt
    find any, it will download the automatically generated subtitles according to the given languages.'''
    
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, cookies="cookies.txt")
    try:
        manual_transcripts = transcript_list.find_manually_created_transcript(languages)
        manual_transcripts = manual_transcripts.fetch()
        return manual_transcripts, video_id
    except:
        print(f"It seeems there are no manually created subtitles for this video: {video_id}.\nLooking for automatically generated subtitles instead")
    #script only reaches this part ⬇ if the manual script wasn't found!
    try:
        auto_transcripts = transcript_list.find_generated_transcript(languages)
        auto_transcripts = auto_transcripts.fetch()
        return auto_transcripts, video_id
    except:
        raise LookupError("I couldn't find any subtitles. Are you sure they are available? Contact me if so and I'll try to help: luil@itu.dk")
    finally:
        print(f"Subtitles have been succesfully extracted for {video_id}")

def save_subtitles(transcript, video_id: str, format: str):
    '''Used to format fetched subtitles into 4 different options
        srt, json, txt and webvtt.
        Outputs a formatted file to the local directory'''
    
    file_name = video_info(video_id)
    formats = ["srt", "json", "txt", "webvtt"]
    
    if format.lower() not in formats:
        raise TypeError("The format you specified is not supported. Only srt, json, txt and webvtt are supported")
    
    elif format.lower() == formats[0]:
        srt_maker = formatter.SRTFormatter()
        srt_formatted = srt_maker.format_transcript(transcript)
        with open(f"{file_name}_subtitles.{format.lower()}", "w", encoding="utf-8") as srt_file:
            srt_file.write(srt_formatted)
            print("srt file saved")

    elif format.lower() == formats[1]:
        json_maker = formatter.JSONFormatter()
        json_formatted = json_maker.format_transcript(transcript)
        with open(f"{file_name}_subtitles.{format.lower()}", "w", encoding="utf-8") as json_file:
            json_file.write(json_formatted)
            print("json file saved")

    elif format.lower() == formats[2]:
        txt_maker = formatter.TextFormatter()
        txt_formatted = txt_maker.format_transcript(transcript)
        with open(f"{file_name}_subtitles.{format.lower()}", "w", encoding="utf-8") as txt_file:
            txt_file.write(txt_formatted)
            print("txt file saved")

    elif format.lower() == formats[3]:
        webvvt_maker = formatter.WebVTTFormatter()
        webvvt_formatted = webvvt_maker.format_transcript(transcript)
        with open(f"{file_name}_subtitles.{format.lower()}", "w", encoding="utf-8") as webvvt_file:
            webvvt_file.write(webvvt_formatted)
            print("webvvt file saved")

    return None


#TODO: Add exception for 403 requests
def video_info(video_id: str) -> str:
    ''' It is currently used to name files according to the title of the video!
    Quick request to obtain information about the video without the need of an YouTube Data V3 key
    It creates a dictionary with different info of which the following might be of interest:
        - Title: title of the video
        - Author name
        - author_url: Name of the channel that uploaded the video
        - thumbnail_url: Could be used for analysis later on'''
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
    return data['title']

#TODO: Implement
def zip_maker(Any):
    return None

