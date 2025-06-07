import sys,os, webbrowser

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

    # context menu 
    def context_menu(self, data):
        return [
            {
                "Title"     : "HELP | Query arguments",
                "SubTitle"  : "click to open in web",
                "IcoPath"   : "Images\\warning.png",
                "Score"     : 1100,
                "JsonRPCAction": {
                    "method"    : "open_url",
                    "parameters": ["https://github.com/Woysful/Media-Downloader/blob/master/README.md#keys-and-temporal-parameters"],
                    "dontHideAfterAction": True
                }
            },
            {
                "Title"     : "-f",
                "SubTitle"  : "video/audio format | ex: -f mp4",
                "IcoPath"   : "Images\\icon.png",
                "Score"     : 1000
            },
            {
                "Title"     : "-yt",
                "SubTitle"  : "yt-dlp command | ex: -yt bv+ba/best",
                "IcoPath"   : "Images\\icon.png",
                "Score"     : 900
            },
            {
                "Title"     : "-ff",
                "SubTitle"  : "ffmpeg postprocessor args | ex: -ff '-c:v copy -c:a aac'",
                "IcoPath"   : "Images\\icon.png",
                "Score"     : 800
            },
            {
                "Title"     : "-d",
                "SubTitle"  : "open domain config file",
                "IcoPath"   : "Images\\icon.png",
                "Score"     : 700
            },
            {
                "Title"     : "-s",
                "SubTitle"  : "open flow launcher settings file",
                "IcoPath"   : "Images\\icon.png",
                "Score"     : 600
            },
            {
                "Title"     : "HELP | Domain config",
                "SubTitle"  : "click to open in web",
                "IcoPath"   : "Images\\warning.png",
                "Score"     : 500,
                "JsonRPCAction": {
                    "method"    : "open_url",
                    "parameters": ["https://github.com/Woysful/Media-Downloader/blob/master/README.md#individual-settings"],
                    "dontHideAfterAction": True
                }
            },
            {
                "Title"     : "yt-dlp parameters",
                "SubTitle"  : "yt-dlp download parameters | ex: bv+ba/best",
                "IcoPath"   : "Images\\config.png",
                "Score"     : 400
            },
            {
                "Title"     : "postprocessor args",
                "SubTitle"  : "ffmpeg postprocessor args | ex: '-c:v copy -c:a aac'",
                "IcoPath"   : "Images\\config.png",
                "Score"     : 300
            },
            {
                "Title"     : "video format",
                "SubTitle"  : "Video stream container | ex: mkv",
                "IcoPath"   : "Images\\config.png",
                "Score"     : 200
            },
            {
                "Title"     : "audio format",
                "SubTitle"  : "Audio stream container | ex: m4a",
                "IcoPath"   : "Images\\config.png",
                "Score"     : 100
            }
        ]

    def open_url(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    media_downloader()