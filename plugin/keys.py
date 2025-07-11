from pyperclip  import paste
from re         import finditer, compile
from os         import startfile, path, makedirs
from sys        import exit

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

def key_check(query):
    key_pattern = r'-(\w+)(?:\s+([^-\s][^-]*))?'
    args = {}
    for match in finditer(key_pattern, query):
        key = match.group(1)
        value = match.group(2).strip() if match.group(2) else None
        args[key] = value

    if query.replace(" ", "") != "":
        for key, value in args.items():
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

    return args, url