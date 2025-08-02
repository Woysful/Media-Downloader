import sys,os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher

class ContextMenu:
    def context_menu(self, data):
        return [
            {
                "Title"     : "Domain Settings",
                "SubTitle"  : "Open config.JSON",
                "IcoPath"   : "Images\\List.png",
                "Score"     : 5000,
                "JsonRPCAction": {
                    "method"    : "open_config",
                    "parameters": [],
                    "dontHideAfterAction": True
                }
            },
            {
                "Title"     : "User Settings",
                "SubTitle"  : "This plugin settings.json file",
                "IcoPath"   : "Images\\config.png",
                "Score"     : 3000,
                "JsonRPCAction": {
                    "method"    : "open_settings",
                    "parameters": [],
                    "dontHideAfterAction": True
                }
            },
            {
                "Title"     : "Logs",
                "IcoPath"   : "Images\\Logs.png",
                "Score"     : 1500,
                "JsonRPCAction": {
                    "method"    : "open_logs",
                    "parameters": [],
                    "dontHideAfterAction": True
                }
            },
            {
                "Title"     : "HELP | Query arguments",
                "SubTitle"  : "click to open in web",
                "IcoPath"   : "Images\\warning.png",
                "Score"     : 500,
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
                "Score"     : 110
            },
            {
                "Title"     : "-q",
                "SubTitle"  : "video quality | ex: -q 1080",
                "IcoPath"   : "Images\\icon.png",
                "Score"     : 100
            },
            {
                "Title"     : "-yt",
                "SubTitle"  : "yt-dlp command | ex: -yt bv+ba/best",
                "IcoPath"   : "Images\\icon.png",
                "Score"     : 90
            },
            {
                "Title"     : "-ff",
                "SubTitle"  : "ffmpeg postprocessor args | ex: -ff '-c:v copy -c:a aac'",
                "IcoPath"   : "Images\\icon.png",
                "Score"     : 80
            },
            {
                "Title"     : "-d",
                "SubTitle"  : "open domain config file",
                "IcoPath"   : "Images\\icon.png",
                "Score"     : 70
            },
            {
                "Title"     : "-s",
                "SubTitle"  : "open flow launcher settings file",
                "IcoPath"   : "Images\\icon.png",
                "Score"     : 60
            },
            {
                "Title"     : "-log",
                "SubTitle"  : "open logs file",
                "IcoPath"   : "Images\\icon.png",
                "Score"     : 50
            },
            {
                "Title"     : "HELP | Domain config",
                "SubTitle"  : "click to open in web",
                "IcoPath"   : "Images\\warning.png",
                "Score"     : 40,
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
                "Score"     : 30
            },
            {
                "Title"     : "postprocessor args",
                "SubTitle"  : "ffmpeg postprocessor args | ex: '-c:v copy -c:a aac'",
                "IcoPath"   : "Images\\config.png",
                "Score"     : 20
            },
            {
                "Title"     : "video format",
                "SubTitle"  : "Video stream container | ex: mkv",
                "IcoPath"   : "Images\\config.png",
                "Score"     : 10
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

    def open_settings(self):
        os.startfile(os.path.expandvars(r"%APPDATA%\FlowLauncher\Settings\Plugins\Media Downloader\settings.json"))

    def open_logs(self):
        file_path = r".\plugin\logs.txt"
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                pass
        os.startfile(file_path)

class ResponseInstall(FlowLauncher, ContextMenu):
    def query(self, query: str):
        key = key_check_ui(query, config)
        if key:
            return key
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
        from plugin.installer import install_ffmpeg, install_ytdlp
        from flowlauncher import FlowLauncherAPI
        import asyncio
        key_check(query, config)
        try:
            yt = asyncio.run(install_ytdlp())
            ff = asyncio.run(install_ffmpeg())
            if yt and ff:
                FlowLauncherAPI.show_msg(title="Components installed!", sub_title="You can continue to use the plugin")
        except:
            sys.exit(1)

class ResponseBadUrl(FlowLauncher, ContextMenu):
    def query(self, query: str):
        key = key_check_ui(query, config)
        if key:
            return key
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
        key_check(query, config)
    
    def check(self, query):
        key_check(query, config)

class ResponseMain(FlowLauncher, ContextMenu):
    def query(self, query: str):
        key = key_check_ui(query, config)
        if key:
            return key
        return [
            {
                "Title"     : "Video",
                "SubTitle"  : config.ui_format_v
                            + config.vid_param_chk
                            + config.ui_quality
                            + config.ui_ytdlp
                            + config.ui_ffmpeg
                            + config.ui_domain,
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
                "SubTitle"  : config.ui_format_a
                            + config.aud_param_chk
                            + config.ui_ytdlp
                            + config.ui_ffmpeg
                            + config.ui_domain,
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
        from plugin.utils import download
        download(button_param, query, config)

    def check(self, query):
        key_check(query, config)

if __name__ == "__main__":
    from plugin.keys import url_valid, key_check, key_check_ui
    from plugin.settings import Config
    valid, url = url_valid()
    config = Config(url)

    if not (os.path.isfile(r".\plugin\yt-dlp.exe") and os.path.isfile(r".\plugin\ffmpeg.exe")):
        ResponseInstall()
    else:
        if not valid:
            ResponseBadUrl()
        else:
            ResponseMain()