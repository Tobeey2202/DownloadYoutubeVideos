# This is a sample Python script.


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'bin')
os.environ["PATH"] += os.pathsep + ffmpeg_path

from pytubefix import YouTube
import ffmpeg
def download_video(link, easy_mode):
    SAVE_PATH = os.path.expanduser("~/Desktop")

    # link of the video to be downloaded

    try:
        # object creation using YouTube
        yt = YouTube(link)
    except:
        #to handle exception
        print("Connection Error")

    # Get all streams and filter for mp4 files
    mp4_streams = yt.streams.filter(file_extension='mp4', progressive = False)
    print(mp4_streams)


    unique_resolutions = set(x.resolution for x in mp4_streams if x.resolution is not None)
    unique_resolutions = list(unique_resolutions)
    numeric_resolutions =[]
    for value in unique_resolutions:
        number = ""
        for x in value:
            if x.isnumeric():
                number += x
        numeric_resolutions.append(int(number))

    numeric_resolutions.sort()

    check = True
    selected_resolution = ''

    if easy_mode =="Y":
        check = False
        selected_resolution = str(numeric_resolutions[-1])
        print(type(selected_resolution))
        print(selected_resolution)

    while check:
        selected_resolution = input(f"Please select a pixel resolution by typing the resolution in full from the following list {numeric_resolutions} \n")
        if int(selected_resolution) in numeric_resolutions:
            print("Thank you for selecting your resolution. Please select a file:")
            break
        else:
            print("Input resolution not available, please try again")

    videos = [x for x in mp4_streams if x.resolution == f"{selected_resolution}p"]
    itags =[]
    print("Itag, Resolution, Codec")
    for video in videos:
        print(video.itag, " ", video.resolution, " ", video.codecs)
        itags.append(int(video.itag))
    print(itags)

    # Download the Video file
    video_itag = ""
    if easy_mode =="Y":
        video_itag = itags[0]

    while check:
        video_itag = input("Please input your itag number \n")
        if int(video_itag) in itags:
            print(video_itag, " found")
            break
        else:
            print("itag not valid, try again please: \n")

    print("Please Choose an audio file")
    audios = [x for x in mp4_streams if x.type == "audio"]
    itags = []
    print("Itag, Bit Rate, Codec")
    for audio in audios:
        print(audio.itag, " ", audio.abr, " ", audio.codecs)
        itags.append(int(audio.itag))
    print(itags)


    # Download the audio file
    audio_itag = ""
    if easy_mode =="Y":
        audio_itag = itags[0]
    while check:
        audio_itag = input("Please input your itag number \n")
        if int(audio_itag) in itags:
            print(audio_itag, " found")
            break
        else:
            print("itag not valid, try again please: \n")

    video_name = yt.streams.get_by_itag(video_itag).default_filename
    # get the video with the highest resolution
    # d_video = mp4_streams[-1]
    # d_video = mp4_streams.first()


    # downloading the video
    # d_video.download(output_path=SAVE_PATH)
    yt.streams.get_by_itag(video_itag).download(filename="video.mp4")
    yt.streams.get_by_itag(audio_itag).download(filename="audio.mp4")


    # Get the directory of the current file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    print("Current directory:", current_directory)

    input_video = ffmpeg.input(rf"{current_directory}\video.mp4")
    input_audio = ffmpeg.input(rf"{current_directory}\audio.mp4")
    print(rf'{SAVE_PATH}\{video_name}')
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(rf'{SAVE_PATH}\{video_name}').run()



    print('Video downloaded successfully!')




link = input("Please Insert Video Link: \n")
while True:
    easy_mode = input("Automatically Download the Highest Quality (Y/N)?")
    if easy_mode.lower() == 'y' or easy_mode.lower() == "n":
        break
    else:
        print("Invalid: Respond with 'Y' or 'N'")
download_video(link, easy_mode.upper())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
