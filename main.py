import sys,os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher
from utils import run

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

    def run_downloader(self, param):
        run(param)

if __name__ == "__main__":
    DownloaderPlugin()
