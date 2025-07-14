from pyperclip  import paste
from re         import finditer, compile
from os         import startfile, path, makedirs
from sys        import exit
from settings   import Config

url = paste().strip()

def url_valid():
    url_pattern = compile(
    r'((http[s]?://)?(www\.)?'
    r'([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}'
    r'(/[^\s]*)?)')
    if not url_pattern.match(url):
        return False, url
    else:
        return True, url
    
# This one is using on each query update. For example when user types in the search box
def key_check_ui(query, config: Config):
    key_pattern = r'-(\w+)(?:\s+([^-\s][^-]*))?'
    keys = {}
    for match in finditer(key_pattern, query):
        key = match.group(1)
        value = match.group(2).strip() if match.group(2) else None
        keys[key] = value
        
    if query.replace(" ", "") != "":
        for key, value in keys.items():
            match key:

                # open config file
                case _key if _key in config.key_list_domain:
                    return [
                        {
                            "Title"     : "Open Domain Config",
                            "SubTitle"  : "Config.json",
                            "IcoPath"   : "Images\\List.png",
                            "JsonRPCAction": {
                                "method"    : "check",
                                "parameters": [query],
                                "dontHideAfterAction": True
                            }
                        }
                    ]

                # open settings file
                case _key if _key in config.key_list_settings: 
                    return [
                        {
                            "Title"     : "Open Settings",
                            "SubTitle"  : "Flow Launcher user settings",
                            "IcoPath"   : "Images\\config.png",
                            "JsonRPCAction": {
                                "method"    : "check",
                                "parameters": [query],
                                "dontHideAfterAction": True
                            }
                        }
                    ]

                # open log file
                case _key if _key in config.key_list_log: 
                    return [
                        {
                            "Title"     : "Open log file",
                            "IcoPath"   : "Images\\Logs.png",
                            "JsonRPCAction": {
                                "method"    : "check",
                                "parameters": [query],
                                "dontHideAfterAction": True
                            }
                        }
                    ]

                # format
                case _key if _key in config.key_list_format:
                    if keys.get(_key): config.ui_format_v   = config.ui_format_a = keys.get(_key)

                # quality
                case _key if _key in config.key_list_quality:
                    if keys.get(_key): config.ui_quality    = " | " + keys.get(_key) + "p"

                # ytdlp parameters
                case _key if _key in config.key_list_ytdlp:
                    if keys.get(_key): config.ui_ytdlp      = " | " + "+YT-dlp"
                
                # ffmpeg parameters
                case _key if _key in config.key_list_ffmpeg:
                    if keys.get(_key): config.ui_ffmpeg     = " | " + "+FFmpeg"

        config.vid_param_chk = ""
        config.aud_param_chk = ""
    else: return False

# This one is using on button press
def key_check(query, config: Config):
    key_pattern = r'-(\w+)(?:\s+(?:"([^"]*)"|\'([^\']*)\'|([^-][^-]*)))?'
    keys = {}
    for match in finditer(key_pattern, query):
        key = match.group(1)
        value = next((g for g in match.groups()[1:] if g), None)
        keys[key] = value

    vid_quality = ""
    if query.replace(" ", "") != "":
        for key, value in keys.items():
            match key:

                # open config file
                case _key if _key in config.key_list_domain:
                    startfile(r".\plugin\config.json")
                    exit(1)

                # open settings file
                case _key if _key in config.key_list_settings: 
                    startfile(path.expandvars(r"%APPDATA%\FlowLauncher\Settings\Plugins\Media Downloader\settings.json"))
                    exit(1)

                # open log file
                case _key if _key in config.key_list_log: 
                    file_path = r".\plugin\logs.txt"
                    if not path.exists(file_path):
                        makedirs(path.dirname(file_path), exist_ok=True)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            pass
                    startfile(file_path)
                    exit(1)

                # quality
                case _key if _key in config.key_list_quality: 
                    quality = keys.get(_key, "")
                    if quality != "":
                        vid_quality = f"bv[height<={quality}]+(ba[ext={config.aud_format}]/ba[ext=m4a]/ba)/".strip()
                
                # format
                case _key if _key in config.key_list_format: 
                    config.vid_format = config.aud_format = keys.get(_key, config.vid_format).strip()
                
                # ytdlp parameters
                case _key if _key in config.key_list_ytdlp: 
                    config.vid_param = keys.get(_key, config.vid_param).strip()
                
                # ffmpeg parameters
                case _key if _key in config.key_list_ffmpeg: 
                    config.ff_param = "'" + keys.get(_key, config.vid_param) + "'"
                    
    return vid_quality, url