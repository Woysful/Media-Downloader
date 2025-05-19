import sys,os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher
from utils import run, config

import subprocess
ffmpeg_path = '.\plugin\\ffmpeg.exe'
ytdlp_path = '.\plugin\\yt-dlp.exe'

class media_downloader(FlowLauncher):
    def query(self, query):
        if not (os.path.isfile(ytdlp_path) and os.path.isfile(ffmpeg_path)):
            installing = [
                {
                    "Title": "Press to install components",
                    "SubTitle": "Download ffmpeg and yt-dlp | it could take some time",
                    "IcoPath": "Images\\warning.png",
                    "Score": 50000,
                    "JsonRPCAction": {
                        "method": "install_components",
                        "parameters": [],
                        "dontHideAfterAction": True
                    }
                }
            ]            
            return installing
        
        elif not config.url:
            empty_clipboard = [
                {
                    "Title": "Copy the link first!",
                    "SubTitle": "Your clipboard is empty, copy a link to media :3",
                    "IcoPath": "Images\\warning.png",
                    "Score": 50000,
                },
                {
                    "Title": "Settings",
                    "SubTitle": "Open config.JSON",
                    "IcoPath": "Images\\config.png",
                    "Score": 0,
                    "JsonRPCAction": {
                        "method": "open_config",
                        "parameters": [],
                        "dontHideAfterAction": True
                    }
                }
            ]
            return empty_clipboard
        
        elif not config.url_pattern.match(config.url):
            wrong_url = [
                {
                    "Title": "No link detected :c",
                    "SubTitle": "You have to copy the link first",
                    "IcoPath": "Images\\warning.png",
                    "Score": 50000,
                },
                {
                    "Title": "Settings",
                    "SubTitle": "Open config.JSON",
                    "IcoPath": "Images\\config.png",
                    "Score": 0,
                    "JsonRPCAction": {
                        "method": "open_config",
                        "parameters": [],
                        "dontHideAfterAction": True
                    }
                }
            ]
            return wrong_url
        
        else:
            buttons = [
                {
                    "Title": "Video",
                    "SubTitle": config.vid_format + " | " + config.domain_visual + config.vid_format_chk,
                    "IcoPath": "Images\\video.png",
                    "Score": 1000000,
                    "JsonRPCAction": {
                        "method": "run_downloader",
                        "parameters": ["video"],
                        "dontHideAfterAction": False
                    }
                },
                {
                    "Title": "Video Best",
                    "SubTitle": "Best | No re-encoding",
                    "IcoPath": "Images\\video_best.png",
                    "Score": 250000,
                    "JsonRPCAction": {
                        "method": "run_downloader",
                        "parameters": ["video_best"],
                        "dontHideAfterAction": False
                    }
                },
                {
                    "Title": "Audio",
                    "SubTitle": config.aud_format + " | " + config.domain_visual + config.aud_format_chk,
                    "IcoPath": "Images\\audio.png",
                    "Score": 750000,
                    "JsonRPCAction": {
                        "method": "run_downloader",
                        "parameters": ["audio"],
                        "dontHideAfterAction": False
                    }
                },
                {
                    "Title": "Audio Best",
                    "SubTitle": "Best | Convert to WAV",
                    "IcoPath": "Images\\audio_best.png",
                    "Score": 50000,
                    "JsonRPCAction": {
                        "method": "run_downloader",
                        "parameters": ["audio_best"],
                        "dontHideAfterAction": False
                    }
                },
                {
                    "Title": "Settings",
                    "SubTitle": "Open config.JSON",
                    "IcoPath": "Images\\config.png",
                    "Score": 0,
                    "JsonRPCAction": {
                        "method": "open_config",
                        "parameters": [],
                        "dontHideAfterAction": True
                    }
                }
            ]
            return buttons

    def run_downloader(self, param):
        run(param)
    
    def install_components(self, *args):
        try:
            subprocess.Popen(['cmd.exe', '/k', f'python installer.py'],creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            sys.exit(1)
    
    def open_config(self):
        os.startfile("config.json")


if __name__ == "__main__":
    media_downloader()