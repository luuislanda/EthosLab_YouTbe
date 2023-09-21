import argparse
import datetime
from models import id_extractor, playlist_link_extractor, text_link_extractor, transcript_getter, save_subtitles, zip_maker
from tqdm import tqdm
import pandas as pd
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

    error_videoids = []

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
        try:
            transcript, id = transcript_getter(video)
            save_subtitles(transcript, id, file_format, subtitles_folder)
        except Exception as e:
            print(f"An error ocurred when processing {video}")
            error_videoids.append(video)

    # Create zip file
    zip_maker(subtitles_folder, f"{subtitles_folder}.zip")


    # Convert the error_videos list to a DataFrame and save to csv
    error_videos_df = pd.DataFrame(error_videoids, columns=['video_id'])
    error_videos_df.to_csv(f'{session_name}_errors.csv', index=False)
    total_errors = len(error_videoids)
    percentage = (total_errors / len(ids_videos)) * 100  # Calculate the percentage

    
    print("Total errors -> " + str(total_errors))  
    print(str(percentage) + "%")  
