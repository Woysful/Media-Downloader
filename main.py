import sys,os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher, FlowLauncherAPI

class ContextMenu:
    def context_menu(self, data):
        return [
            {
                "Title"     : "Domain Settings",
                "SubTitle"  : "Open config.JSON",
                "IcoPath"   : "Images\\config.png",
                "Score"     : 10000,
                "JsonRPCAction": {
                    "method"    : "open_config",
                    "parameters": [],
                    "dontHideAfterAction": True
                }
            },
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
                "Title"     : "-log",
                "SubTitle"  : "open logs file",
                "IcoPath"   : "Images\\icon.png",
                "Score"     : 500
            },
            {
                "Title"     : "HELP | Domain config",
                "SubTitle"  : "click to open in web",
                "IcoPath"   : "Images\\warning.png",
                "Score"     : 400,
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
                "Score"     : 300
            },
            {
                "Title"     : "postprocessor args",
                "SubTitle"  : "ffmpeg postprocessor args | ex: '-c:v copy -c:a aac'",
                "IcoPath"   : "Images\\config.png",
                "Score"     : 200
            },
            {
                "Title"     : "video format",
                "SubTitle"  : "Video stream container | ex: mkv",
                "IcoPath"   : "Images\\config.png",
                "Score"     : 100
            },
            {
                "Title"     : "audio format",
                "SubTitle"  : "Audio stream container | ex: m4a",
                "IcoPath"   : "Images\\config.png",
                "Score"     : 0
            }
        ]
    
    def open_url(self, help_url):
        from webbrowser import open
        open(help_url)
        
    def open_config(self):
        os.startfile(r".\plugin\config.json")

class Install(FlowLauncher, ContextMenu):
    def query(self, query: str):
        return [
            {
                "Title"     : "Press to install components",
                "SubTitle"  : "It could take a few minutes. Please wait",
                "IcoPath"   : "Images\\warning.png",
                "JsonRPCAction": {
                    "method"    : "install_components",
                    "parameters": [query],
                    "dontHideAfterAction": True
                }
            }
        ]
    
    def context_menu(self, data):
        return ContextMenu.context_menu(self, data)

    def install_components(self, query, *args):
        from subprocess import Popen, CalledProcessError, CREATE_NEW_CONSOLE
        from plugin.installer import install_ffmpeg, install_ytdlp
        import asyncio
        key_check(query)
        try:
            yt = asyncio.run(install_ytdlp())
            ff = asyncio.run(install_ffmpeg())
            if yt and ff:
                FlowLauncherAPI.show_msg(title="Components installed!", sub_title="You can continue to use the plugin")
        except CalledProcessError:
            sys.exit(1)

class Bad_Url(FlowLauncher, ContextMenu):
    def query(self, query: str):
        return [
            {
                "Title"     : "No link detected :c",
                "SubTitle"  : "You have to copy the link first",
                "IcoPath"   : "Images\\warning.png",
                "JsonRPCAction": {
                    "method"    : "args",
                    "parameters": [query],
                    "dontHideAfterAction": True
                }
            }
        ]
    
    def context_menu(self, data):
        return ContextMenu.context_menu(self, data)

    def args(self, query):
        key_check(query)

class Main(FlowLauncher, ContextMenu):
    def query(self, query: str):
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
            }
        ]
    
    def context_menu(self, data):
        return ContextMenu.context_menu(self, data)

    def run_downloader(self, button_param, query):
        from plugin.utils import run_d
        run_d(button_param, query, config)

if __name__ == "__main__":
    from plugin.keys import url_valid, key_check

    if not (os.path.isfile(r".\plugin\yt-dlp.exe") and os.path.isfile(r".\plugin\ffmpeg.exe")):
        Install()
    else:
        valid, url = url_valid()
        if not valid:
            Bad_Url()
        else:
            from plugin.settings import Cfg
            config = Cfg(url)
            
            Main()