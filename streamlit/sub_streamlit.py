import streamlit as st
from models import id_extractor, playlist_link_extractor, text_link_extractor, transcript_getter, save_subtitles, zip_maker

st.title("Experimental super secret tool for Jess 🤫")

st.header("Youtube Subtitle Downloader")

st.markdown("This is a very minimal deployment of the subtitle extractor tool. At the moment, the script only works with the following:")

st.markdown("* Txt files. For example if you have a bibliography, paste the content to a txt file and upload that file")

st.markdown("* Youtube playlist links. Just paste the link in the form :) ")

st.markdown("The tool will generate a zip file containing subtitles for all available videos. You can select which format to use for the subtitles")
st.text('''Here is an explanation for each file format:
        - txt - a txt file with a monoblock of text. Good for text analysis
        - srt - time stamped subtitle file. Good for re-using subtitles or correcting them
        - json - standard nested json file. Works great for web apps and web things
        - webvtt - metadata and format rich alternative for srt. Good for hipsters and HTML5 devs
        ''')


st.markdown("This version of the script has the following limitations that are actively being worked on: ")
st.markdown("* Super annoying error when playlist field is empty, but doesnt break anything")
st.markdown("* If a playlist or video in text file is not available/deleted/hidden/geo-restricted, the code will break. My mechanism to bypass this doesn't work in the web app but it does offline so this is top priority that is very fixable!")
st.markdown("* Super annoying error when the playlist link box is empty ")
st.markdown("* Figuring out how to do logging with this interface, it works offline but needs adjustment for web app")
st.markdown("* No ability to download from single youtube video urls. Need to write code for it")
st.markdown("* No PDF support. Converting to txt manually is not ideal, PDF reading is non-trivial though so it probably will take a few hours to write code for it. Also maybe add support for doc/docx?")
st.markdown("* Generally not a UI/UX person so some feedback on general use and presentation of the tool is very welcome!")
st.markdown("* User has to click twice to download subtiltes, once to generate the file and another to download it. This is due to the streamlit webframework's restrictions. Nothing crazy but ideally we wouldn't click ")
st.markdown("* File uploader is a bit dodgy and not tested as throroughly as plylist. Might not be worth it when moving the tool elsewhere")
st.markdown("* Some errors I haven't know yet. So please let me know of some things")


st.header("Enough about this tool, let's download some subtitles")

option = st.selectbox(
        "Choose the format you will be uploading",
        ('Txt file', 'Youtube playlist URL'))

if option == "Youtube playlist URL":
    st.markdown(":orange[If you see an error below, it's because the playlist field is empty. So add your playlist link and it will go away! I am working on avoiding that but for now it only complains that it is empty. If you any errors after you click on Generate those are the 'proper' code breaking errors. I am sure I can find a way around this annoying error but since it doesnt fully break it it is not a priority :^)] ")


session_name = st.text_input("Write a name for your session and eventual zip file")

file_format = st.selectbox("Choose the format for the subtitle files",
                           ("txt", "srt", "json", "webvtt"))
input_value = ""
ids_videos = []


if option == 'Youtube playlist URL':
    input_value = st.text_input("Input the youtube playlist link")
    ids_videos = id_extractor(playlist_link_extractor(input_value))
elif option == 'Txt file':
    input_value = st.file_uploader("Upload your txt file here")
    if input_value is not None:
        ids_videos = id_extractor(text_link_extractor(input_value))

def generate_file(ids_videos):
    with st.spinner("Workin on it..."):
        for video in ids_videos:
            transcript, id = transcript_getter(video)
            save_subtitles(transcript, id, file_format, session_name)
        st.markdown("**Processed transcripts succesfully. Ready for download**")
    st.success("Woooo Done!")
    zip_maker(session_name, f"{session_name}.zip")

st.markdown("## Generate and download processed files")
if st.button('generate file for download'):
    generate_file(ids_videos)

    with open(f"{session_name}.zip", 'rb') as file:
        st.download_button("Download subtitles", file, file_name=f"{session_name}.zip")

