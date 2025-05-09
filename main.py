import sys,os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

import subprocess, json, pyperclip
from flowlauncher import FlowLauncher

class DownloaderPlugin(FlowLauncher):
    def query(self, query):   
        buttons = [
            {
                "Title": "Video",
                "SubTitle": "your parameters",
                "IcoPath": "Images\\video.png",
                "JsonRPCAction": {
                    "method": "run_downloader",
                    "parameters": ["video"],
                    "dontHideAfterAction": False
                }
            },
            {
                "Title": "Video Best",
                "SubTitle": "webm / vorbis / opus",
                "IcoPath": "Images\\video_best.png",
                "JsonRPCAction": {
                    "method": "run_downloader",
                    "parameters": ["video_best"],
                    "dontHideAfterAction": False
                }
            },
            {
                "Title": "Audio",
                "SubTitle": "your parameters",
                "IcoPath": "Images\\audio.png",
                "JsonRPCAction": {
                    "method": "run_downloader",
                    "parameters": ["audio"],
                    "dontHideAfterAction": False
                }
            },
            {
                "Title": "Audio Best",
                "SubTitle": "vorbis / opus --> wav",
                "IcoPath": "Images\\audio_best.png",
                "JsonRPCAction": {
                    "method": "run_downloader",
                    "parameters": ["audio_best"],
                    "dontHideAfterAction": False
                }
            }
        ]
        return buttons

    def run_downloader(self, mode):
        def load_config(config_path="config.json"):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                return config
            except Exception as e:
                return {}

        config = load_config()

        download_directory  = config.get("download_directory", ".")
        video_format        = config.get("preferred_video_format", "mkv")
        audio_output_format = config.get("preferred_audio_format", "m4a")
        video_dwnld_param   = config.get("video download parameters", "bv[vcodec^=hev1]+ba[ext=m4a]/bv[vcodec^=avc1]+ba[ext=m4a]")
        
        url = pyperclip.paste().strip()
        if not url:
            sys.exit(1)

        output_template = os.path.join(download_directory, "%(title)s.%(ext)s")

        if mode == "video":
            command = ['yt-dlp.exe', '-f', video_dwnld_param, '-o', output_template, '--remux-video', video_format, '--embed-metadata', url]
        elif mode == "video_best":
            command = ['yt-dlp.exe', '-f', 'bestvideo+bestaudio/best', '-o', output_template, url]
        elif mode == "audio":
            command = ['yt-dlp.exe', '-f', 'bestaudio', '-x', '--audio-format', audio_output_format, '-o', output_template, url]
        elif mode == "audio_best":
            command = ['yt-dlp.exe', '-f', 'bestaudio', '-x', '--audio-format', 'wav', '-o', output_template, url]
        else:
            sys.exit(1)

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            sys.exit(1)

if __name__ == "__main__":
    DownloaderPlugin()
