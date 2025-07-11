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
                case _key if _key in config.key_list_format:
                    if keys.get(_key):
                        config.ui_format_v = config.ui_format_a = keys.get(_key)
                case _key if _key in config.key_list_quality:
                    if keys.get(_key): config.ui_quality = " | " + keys.get(_key) + "p"
                case _key if _key in config.key_list_ytdlp:
                    if keys.get(_key): config.ui_ytdlp = " | " + "YTDLP param"
                case _key if _key in config.key_list_ffmpeg:
                    if keys.get(_key): config.ui_ffmpeg = " | " + "FFmpeg param"
        config.vid_param_chk = ""
        config.aud_param_chk = ""

def key_check(query):
    key_pattern = r'-(\w+)(?:\s+([^-\s][^-]*))?'
    keys = {}
    for match in finditer(key_pattern, query):
        key = match.group(1)
        value = match.group(2).strip() if match.group(2) else None
        keys[key] = value

    if query.replace(" ", "") != "":
        for key, value in keys.items():
            match key:
                case 'd' | 'D' | 'domain' | 'Domain' | 'DOMAIN':
                    startfile(r".\plugin\config.json")
                    exit(1)
                case 's' | 'S' | 'settings' | 'SETTINGS':
                    startfile(path.expandvars(r"%APPDATA%\FlowLauncher\Settings\Plugins\Media Downloader\settings.json"))
                    exit(1)
                case 'l' | 'log' | 'logs' | 'Log' | 'Logs' | 'LOG' | 'LOGS':
                    file_path = r".\plugin\logs.txt"
                    if not path.exists(file_path):
                        makedirs(path.dirname(file_path), exist_ok=True)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            pass
                    startfile(file_path)
                    exit(1)
    return keys, url