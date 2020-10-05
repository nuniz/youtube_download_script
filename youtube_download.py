from pytube import YouTube
from pytube import Playlist
import sys
import re
import configparser
import os
from safe_name import *


def str_to_bool(string):
    if string == "True":
        return True
    else:
        return False


def print_list(_list):
    for i in range (len(_list)): 
        print(_list[i])
    print ('\n')


def download_video(
                    youtube_video_urls,
                    download_path,
                    url_regex,
                    audio_flag = True,
                    playlist_flag = False):

    if youtube_video_urls is None:
        sys.exit('ERROR: No youtube_video_urls')

    if str(type(youtube_video_urls)) == "<class 'str'>":
        youtube_video_urls = [youtube_video_urls]
    for youtube_video_url in youtube_video_urls:
        if not (re.match(url_regex, youtube_video_url) is not None):
            raise ValueError("URL is not valid: " + youtube_video_url)
            pass
            
        print ('*******\n' + youtube_video_url)
        
        try:
            if playlist_flag:
                playlist = Playlist(str(youtube_playlist_url))
            else:
                playlist = YouTube(str(youtube_video_url))
            for yt_obj in playlist:
                filters = yt_obj.streams.filter(progressive=True, 
                                                file_extension='mp4')
                filename = clean_filename(yt_obj.title)
                fullfilename = os.path.join(download_path, 
                                            filename)
                if audio_flag:
                    print('Save: ' + filename)
                    filters = yt_obj.streams.get_audio_only().download(filename = filename,
                                                                       output_path = download_path)
                    os.system('ffmpeg -i {} -acodec pcm_s16le -ar 16000 {}.wav'.format(fullfilename+'.mp4',
                                                                                       fullfilename))
                    os.remove(fullfilename + '.mp4')
                else:
                    filters.get_highest_resolution().download(output_path = download_path)
                print(f'{yt_obj.title} Downloaded Successfully')

        except Exception as e:
            print('Exception: ' + str(e))


if __name__ == "__main__":
    url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    
    config = configparser.ConfigParser()
    config.read('config.ini')
    download_path = config['DEFAULT'].get('download_path')
    audio_flag = str_to_bool(config['DEFAULT'].get('audio_flag'))
    youtube_video_urls_string = config['youtube_urls'].get('youtube_video_urls').splitlines()
    youtube_playlist_url_string = config['playlist_urls'].get('youtube_playlist_url').splitlines()
    
    
    print('Download Path is: ' + download_path)
    
    if audio_flag:
        print('Download As Audio\n')
    else:
        print('Download Videos')
    
    
    if len(youtube_video_urls_string) > 1:
        youtube_video_urls = youtube_video_urls_string[1:]
        print ('~~~~~~~~~~~~~~~~~~')
        print('Download Youtube Videos \n')
        print_list(youtube_video_urls)
        download_video(youtube_video_urls, 
                       download_path, 
                       url_regex, 
                       audio_flag)
        print('All YouTube downloaded successfully. \n')
    
    
    if len(youtube_playlist_url_string) > 1:
        youtube_playlist_url = youtube_playlist_url_string[1:]
        print ('~~~~~~~~~~~~~~~~~~')
        print('Download Youtube Playlist')
        print_list(youtube_playlist_url)
        for i in range(len(youtube_playlist_url)):
            download_video(youtube_playlist_url[i], 
                              download_path, 
                              url_regex, 
                              audio_flag,
                              playlist_flag = True)
        print('YouTube Playlist downloaded successfully. \n')

    x=2