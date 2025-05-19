import sys, os, subprocess, pyperclip, json, tldextract, shlex, re, winsound
from datetime import datetime

# getting config settings
class config():
    def load_config(config_path="config.json"):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            return config
        except Exception as e:
            return {}

    def load_settings(settings_path = os.path.expandvars(r'%APPDATA%\FlowLauncher\Settings\Plugins\Media Downloader\settings.json')):
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            return config
        except Exception as e:
            return {}
    
    # getting and validating URL from clipboard
    url = pyperclip.paste().strip()
    url_pattern = re.compile(
    r'((http[s]?://)?(www\.)?'
    r'([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}'
    r'(/[^\s]*)?)')

    # extracting domain from URL
    def extract_domain(url) -> str:
        extracted = tldextract.extract(url)
        domain = extracted.domain
        return domain
    
    config_full     = load_config()
    settings_full   = load_settings()
    
    output_path     = os.path.join(settings_full.get("download_directory", "%USERPROFILE%\Downloads"), "%(title)s.%(ext)s")    
    vid_format      = config_full.get("preferred_video_format", "mkv")
    aud_format      = config_full.get("preferred_audio_format", "m4a")
    vid_param_def   = config_full.get("default_video_parameters", "bv+ba/best")
    sound           = config_full.get("download_complete_sound", True)
    
    domains_conf    = config_full.get("domains", {})
    domain          = extract_domain(url)
    domain_param    = domains_conf.get(domain, {})
    vid_param       = domain_param.get("yt-dlp parameters", vid_param_def)
    arg_param       = domain_param.get("postprocessor args", "")

    ytdlp_path  = '.\plugin\yt-dlp.exe'

# running the whole thing
def run(param):    
    # forming yt-dlp command based on button that user pressed
    match param:
        case "video":
            command = [config.ytdlp_path, config.url,
                       '-o', config.output_path,
                       '-f', config.vid_param,
                       '--merge-output-format', config.vid_format,
                       '--embed-metadata']
        case "video_best":
            command = [config.ytdlp_path, config.url, '-o', config.output_path,
                       '-f', 'bestvideo+bestaudio/best']
        case "audio":
            command = [config.ytdlp_path, config.url, '-o', config.output_path,
                       '-f', 'bestaudio',
                       '-x', '--audio-format', config.aud_format]
        case "audio_best":
            command = [config.ytdlp_path, config.url, '-o', config.output_path,
                       '-f', 'bestaudio',
                       '-x', '--audio-format', 'wav']
        case _:
            sys.exit(1)

    # if this domain has postprocessor arguments in config
    try:
        if config.arg_param:
            command = [config.ytdlp_path,
                       '-f', config.vid_param,
                       '--merge-output-format', config.vid_format,                       
                       '--postprocessor-args'] + shlex.split(config.arg_param) + [
                        '-o', config.output_path, 
                        '--embed-metadata',
                        config.url]

            with open("logs.txt", "a", encoding="utf-8") as f:
                f.write("\nTime: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                f.write("\nDomain: " + config.domain)
                f.write("\nLink: " + config.url)
                f.write("\nCommand with args: " + str(command) + "\n")

            subprocess.run(command, check=True)
            if config.sound == True:
                winsound.PlaySound(r'.\sound\done.wav', winsound.SND_FILENAME)
        else:
            with open("logs.txt", "a", encoding="utf-8") as f:
                f.write("\nTime: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                f.write("\nDomain: " + config.domain)
                f.write("\nLink: " + config.url)
                f.write("\nCommand: " + str(command) + "\n")

            subprocess.run(command, check=True)
            if config.sound == True:
                winsound.PlaySound(r'.\sound\done.wav', winsound.SND_FILENAME)
    except subprocess.CalledProcessError as e:
        sys.exit(1)