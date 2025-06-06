import sys,os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher       import FlowLauncher
from plugin.utils       import run_d, query_keys
from plugin.settings    import Cfg
from subprocess         import Popen, CREATE_NEW_CONSOLE

config = Cfg()

class media_downloader(FlowLauncher):
    def query(self, query: str):
        # check if ffmpeg and yt-dlp are installed
        if not (os.path.isfile(config.ytdlp_path) and os.path.isfile(config.ffmpeg_path)):
            return [
                {
                    "Title"     : "Press to install components",
                    "SubTitle"  : "Download ffmpeg and yt-dlp | it could take some time",
                    "IcoPath"   : "Images\\warning.png",
                    "Score"     : 50000,
                    "JsonRPCAction": {
                        "method"    : "install_components",
                        "parameters": [query],
                        "dontHideAfterAction": True
                    }
                }
            ]            
        
        # check if clipboard isn't empty
        elif not config.url:
            return [
                {
                    "Title"     : "Copy the link first!",
                    "SubTitle"  : "Your clipboard is empty, copy a link to media :3",
                    "IcoPath"   : "Images\\warning.png",
                    "Score"     : 50000,
                    "JsonRPCAction": {
                        "method"    : "args",
                        "parameters": [query],
                        "dontHideAfterAction": True
                    }
                },
                {
                    "Title"     : "Domain Settings",
                    "SubTitle"  : "Open config.JSON",
                    "IcoPath"   : "Images\\config.png",
                    "Score"     : 0,
                    "JsonRPCAction": {
                        "method"    : "open_config",
                        "parameters": [query],
                        "dontHideAfterAction": True
                    }
                }
            ]
        
        # validate URL
        elif not config.url_pattern.match(config.url):
            return [
                {
                    "Title"     : "No link detected :c",
                    "SubTitle"  : "You have to copy the link first",
                    "IcoPath"   : "Images\\warning.png",
                    "Score"     : 50000,
                    "JsonRPCAction": {
                        "method"    : "args",
                        "parameters": [query],
                        "dontHideAfterAction": True
                    }
                },
                {
                    "Title"     : "Domain Settings",
                    "SubTitle"  : "Open config.JSON",
                    "IcoPath"   : "Images\\config.png",
                    "Score"     : 0,
                    "JsonRPCAction": {
                        "method"    : "open_config",
                        "parameters": [query],
                        "dontHideAfterAction": True
                    }
                }
            ]
        
        # main buttons
        else:
            return [
                {
                    "Title"     : "Video",
                    "SubTitle"  : config.vid_format + " | " + config.domain_visual + config.vid_param_chk,
                    "IcoPath"   : "Images\\video.png",
                    "Score"     : 1000000,
                    "JsonRPCAction": {
                        "method"    : "run_downloader",
                        "parameters": ["video", query],
                        "dontHideAfterAction": False
                    }
                },
                {
                    "Title"     : "Video Best",
                    "SubTitle"  : "Best | No re-encoding",
                    "IcoPath"   : "Images\\video_best.png",
                    "Score"     : 250000,
                    "JsonRPCAction": {
                        "method"    : "run_downloader",
                        "parameters": ["video_best", query],
                        "dontHideAfterAction": False
                    }
                },
                {
                    "Title"     : "Audio",
                    "SubTitle"  : config.aud_format + " | " + config.domain_visual + config.aud_param_chk,
                    "IcoPath"   : "Images\\audio.png",
                    "Score"     : 750000,
                    "JsonRPCAction": {
                        "method"    : "run_downloader",
                        "parameters": ["audio", query],
                        "dontHideAfterAction": False
                    }
                },
                {
                    "Title"     : "Audio Best",
                    "SubTitle"  : "Best | Convert to WAV",
                    "IcoPath"   : "Images\\audio_best.png",
                    "Score"     : 50000,
                    "JsonRPCAction": {
                        "method"    : "run_downloader",
                        "parameters": ["audio_best", query],
                        "dontHideAfterAction": False
                    }
                },
                {
                    "Title"     : "Domain Settings",
                    "SubTitle"  : "Open config.JSON",
                    "IcoPath"   : "Images\\config.png",
                    "Score"     : 0,
                    "JsonRPCAction": {
                        "method"    : "open_config",
                        "parameters": [query],
                        "dontHideAfterAction": True
                    }
                }
            ]

    def run_downloader(self, param, query):
        run_d(param, query, config)
    
    def install_components(self, query, *args):
        query_keys(query, config)
        try:
            Popen(['cmd.exe', '/k', f'python .\plugin\installer.py'],creationflags=CREATE_NEW_CONSOLE)
        except:
            sys.exit(1)
    
    def open_config(self, query):
        query_keys(query, config)
        os.startfile(config.config_path)

    def args(self, query):
        query_keys(query, config)


if __name__ == "__main__":
    media_downloader()