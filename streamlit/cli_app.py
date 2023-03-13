import argparse
import datetime
from models import id_extractor, playlist_link_extractor, text_link_extractor, transcript_getter, save_subtitles, zip_maker
from tqdm import tqdm
from colorama import Fore, Style

if __name__ == "__main__":
    print(f"{Style.BRIGHT}\nStarting the script 🤖 for any weird errors email me at luil@itu.dk or help me out by checking the github \n{Style.RESET_ALL}")
    parser = argparse.ArgumentParser(description='Downloads a zip file containing a copy of a Youtube video(s) transcript(s)')
    parser.add_argument('-i', '--input', help='input. Accepts: file path or URL')
    parser.add_argument('-f', '--format', choices=['srt', 'json', 'txt', 'webvtt'], default='srt',
                        help='You can only choose between srt, json, txt and webvtt. If you are doing text analysis srt and txt are your go-tos.')
    parser.add_argument('-n', '--name', help='Choose a name for the session/zipfile')

    args = parser.parse_args()

    input_value = args.input
    file_format = args.format
    session_name = args.name

    # Set subtitles folder name
    if session_name:
        subtitles_folder = session_name
    else:
        now = datetime.datetime.now()
        subtitles_folder = f'{file_format}_{now.strftime("%Y-%m-%d_%H-%M-%S")}'

    # Check if input is a URL or file path
    if args.input.startswith('http'):
        ids_videos = id_extractor(playlist_link_extractor(input_value))
    else:
        ids_videos = id_extractor(text_link_extractor(input_value))

    # Get transcripts and save subtitles
    for video in tqdm(ids_videos, desc=f"{Fore.YELLOW}{Style.BRIGHT}Downloading transcripts...{Style.RESET_ALL}", unit="video"):
        transcript, id = transcript_getter(video)
        save_subtitles(transcript, id, file_format, subtitles_folder)

    # Create zip file
    zip_maker(subtitles_folder, f"{subtitles_folder}.zip")

