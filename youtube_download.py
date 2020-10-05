from pytube import YouTube
from pytube import Playlist
import sys
import re
import configparser


def print_list(_list):
    for i in range (len(_list)): 
        print(_list[i])
    print ('\n')


def download_video(
                    youtube_video_urls,
                    download_dir,
                    url_regex,
                    audio_flag = True):

    if youtube_video_urls is None:
        sys.exit('ERROR: No youtube_video_urls')

    for youtube_video_url in youtube_video_urls:
        if not (re.match(url_regex, youtube_video_url) is not None):
            raise ValueError("URL is not valid: " + youtube_video_url)
            pass
            
        print ('*******\n' + youtube_video_url)
        
        try:
            yt_obj = YouTube(str(youtube_video_url))
            filters = yt_obj.streams.filter(progressive=True, file_extension='mp4')
            if audio_flag:
                filters = yt_obj.streams.get_audio_only().download(output_path = download_dir)
                
            else:
                filters.get_highest_resolution().download(output_path = download_dir)
            print(f'{yt_obj.title} Downloaded Successfully')

        except Exception as e:
            print(e)


def download_playlist(
                        youtube_playlist_url,
                        download_dir,
                        url_regex,
                        youtube_steam = '140',
                        audio_flag = True):

    if youtube_playlist_url is None:
        sys.exit('ERROR: No youtube_playlist_url.')
        
    if not (re.match(url_regex, youtube_playlist_url) is not None):
            raise ValueError("URL is not valid: " + youtube_playlist_url)
            return

    try:
        playlist = Playlist(youtube_playlist_url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        print(f'Number of videos: {len(playlist.video_urls)}')
        
        for yt_obj in playlist.videos:
            filters = yt_obj.streams.filter(progressive=True, file_extension='mp4')
            if audio_flag:
                filters = yt_obj.streams.get_audio_only().download(output_path = download_dir)
            else:
                filters.get_highest_resolution().download(output_path = download_dir)
            print(f'{yt_obj.title} Downloaded Successfully')
            
        # playlist.download_all(download_dir=download_dir)
     
    except Exception as e:
        print(e)


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
    download_dir = config['DEFAULT'].get('download_dir')
    audio_flag = config['DEFAULT'].get('audio_flag')
    youtube_video_urls_string = config['youtube_urls'].get('youtube_video_urls').splitlines()
    youtube_playlist_url_string = config['playlist_urls'].get('youtube_playlist_url').splitlines()
    
    
    if download_dir is None:
        sys.exit('download_dir is None')
    else:
        print('Download Dir is: ' + download_dir)
    if audio_flag:
        print('Download As Audio\n')
    else:
        print('Download Videos')
    
    
    if len(youtube_video_urls_string)>1:
        youtube_video_urls = youtube_video_urls_string[1:]
        print ('~~~~~~~~~~~~~~~~~~')
        print('Download Youtube Videos \n')
        print_list(youtube_video_urls)
        download_video(youtube_video_urls, download_dir, url_regex)
        print('All YouTube downloaded successfully. \n')
    
    
    if len(youtube_playlist_url_string) > 2:
        youtube_playlist_url = youtube_playlist_url_string[1:]
        print ('~~~~~~~~~~~~~~~~~~')
        print('Download Youtube Playlist')
        print_list(youtube_playlist_url)
        for i in range (len(youtube_playlist_url)): 
            download_playlist(youtube_playlist_url[i], download_dir, url_regex)
            print('YouTube Playlist downloaded successfully. \n')

    x=2