import sys, os, subprocess, pyperclip, json, tldextract, shlex, re, winsound
from datetime import datetime

# getting config settings
class config():
    # config in plugin's folder that has most of the settings
    def load_config(config_path="config.json"):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            return config
        except Exception as e:
            return {}

    # native flow launcher settings file. For now contains only downloading path
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
    vid_format_def  = config_full.get("default video format", "mkv")
    aud_format_def  = config_full.get("default audio format", "m4a")
    vid_param_def   = config_full.get("default video parameters", "bv+ba/best")
    sound           = config_full.get("download complete sound", True)
    
    domains_conf    = config_full.get("domains", {})
    domain          = extract_domain(url)
    
    # edits domain to separate a hand-fixed good visual domain name for buttons
    # and a working one that just covers double domains like youtu.be and youtube.com
    def domain_edit(domain, rep):
        if domain in rep:
            return rep[domain]
        else:
            return domain
    
    domain_visual_rep = {
    "youtu"     : "YouTube",
    "x"         : "Twitter",
    "bsky"      : "Bluesky",
    "tumblr"    : "Tumblr"
    }

    domain_visual = domain_edit(domain, domain_visual_rep)

    domain_work_rep = {
    "youtu": "youtube"
    }

    domain_work = domain_edit(domain, domain_work_rep)

    domain_param    = domains_conf.get(domain_work, {})

    vid_format      = domain_param.get("video format", vid_format_def)
    vid_param       = domain_param.get("yt-dlp parameters", vid_param_def)
    aud_format      = domain_param.get("audio format", aud_format_def)
    arg_param       = domain_param.get("postprocessor args", "")

    # check if this parameter written for this domain. made this for good visual on buttons
    def param_check(domain_param):
        if not domain_param:
            return " | Default settings"
        else:
            return ""
        
    vid_param_chk  = param_check(domain_param)
    aud_param_chk  = param_check(domain_param)

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