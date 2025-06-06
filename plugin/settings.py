from os         import path
from re         import compile
from json       import load
from pyperclip  import paste
from tldextract import extract

# getting config settings
class cfg():
    # config in plugin's folder that has most of the settings
    config_path=".\plugin\config.json"
    def load_config(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = load(f)
            return config
        except:
            return {}

    # native flow launcher settings file
    settings_path = path.expandvars(r'%APPDATA%\FlowLauncher\Settings\Plugins\Media Downloader\settings.json')
    def load_settings(settings_path):
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = load(f)
            return settings
        except:
            return {}
    
    # getting and validating URL from clipboard
    url = paste().strip()
    url_pattern = compile(
    r'((http[s]?://)?(www\.)?'
    r'([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}'
    r'(/[^\s]*)?)')

    # extracting domain from URL
    def extract_domain(url) -> str:
        extracted = extract(url)
        domain = extracted.domain
        return domain
    
    config_full     = load_config(config_path)
    settings_full   = load_settings(settings_path)
    
    output_path     = path.join(settings_full.get("download_directory", "%USERPROFILE%\Downloads"), "%(title)s.%(ext)s")    
    vid_format_def  = settings_full.get("default_video_format", "mkv")
    aud_format_def  = settings_full.get("default_audio_format", "m4a")
    vid_param_def   = settings_full.get("default_video_parameters", "bv+ba/best")
    sound           = settings_full.get("download_complete_sound", True)
    
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
    "youtube"   : "Youtube",
    "x"         : "Twitter",
    "bsky"      : "Bluesky",
    "tumblr"    : "Tumblr",
    "instagram" : "Instagram",
    "vimeo"     : "Vimeo",
    "tiktok"    : "Tiktok"
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
    ff_param        = domain_param.get("postprocessor args", "")

    # check if this parameter written for this domain. made this for good visual on buttons
    def param_check(domain_param):
        if not domain_param:
            return " | Default settings"
        else:
            return ""
        
    vid_param_chk   = param_check(domain_param)
    aud_param_chk   = param_check(domain_param)

    ffmpeg_path     = '.\plugin\\ffmpeg.exe'
    ytdlp_path      = '.\plugin\\yt-dlp.exe'