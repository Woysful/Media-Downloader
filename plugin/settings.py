from os             import path
from json           import load
from urllib.parse   import urlparse

class Cfg:
    def __init__(self, url):
        # settings path
        self.config_path    = r".\plugin\config.json"
        self.settings_path  = path.expandvars(r"%APPDATA%\FlowLauncher\Settings\Plugins\Media Downloader\settings.json")

        # ffmpeg and yt-dlp path
        self.ffmpeg_path    = r".\plugin\ffmpeg.exe"
        self.ytdlp_path     = r".\plugin\yt-dlp.exe"
        
        # load domain config and Flow Launcher settings
        self.config_full    = self.load_json(self.config_path)
        self.settings_full  = self.load_json(self.settings_path)

        # getting user parameters from FL settings file
        self.output_path    = path.join(self.settings_full.get("download_directory", "%USERPROFILE%\\Downloads"), "%(title)s.%(ext)s")
        self.vid_format_def = self.settings_full.get("default_video_format", "mkv")
        self.aud_format_def = self.settings_full.get("default_audio_format", "m4a")
        self.vid_param_def  = self.settings_full.get("default_video_parameters", "bv+ba/best")
        self.sound          = self.settings_full.get("download_complete_sound", True)

        # getting domain name from URL and Domain settings from config.json
        self.domain         = self.get_domain(url)
        self.domains_conf   = self.config_full.get("domains", {})

        # covering doubles
        self.domain_work = self.domain_edit(self.domain, {
            "youtu": "youtube"
        })

        # covering good visual
        self.domain_visual  = self.domain_edit(self.domain, {
            "youtu"     : "YouTube",
            "youtube"   : "Youtube",
            "x"         : "Twitter",
            "bsky"      : "Bluesky",
            "tumblr"    : "Tumblr",
            "instagram" : "Instagram",
            "vimeo"     : "Vimeo",
            "tiktok"    : "Tiktok"
        })

        # getting domain-individual settings from config.json
        domain_param        = self.domains_conf.get(self.domain_work, {})
        self.vid_format     = domain_param.get("video format", self.vid_format_def)
        self.vid_param      = domain_param.get("yt-dlp parameters", self.vid_param_def)
        self.aud_format     = domain_param.get("audio format", self.aud_format_def)
        self.ff_param       = domain_param.get("postprocessor args", "")

        self.vid_param_chk  = self.param_check(domain_param)
        self.aud_param_chk  = self.param_check(domain_param)
    
    # load settings
    def load_json(self, path_):
        try:
            with open(path_, "r", encoding="utf-8") as f:
                return load(f)
        except:
            return {}

    # edits domain to separate a hand-fixed good visual domain name for buttons
    # and a working one that just covers double domains like youtu.be and youtube.com
    def domain_edit(self, domain, rep):
        return rep.get(domain, domain)
    
    # getting domain name from URL
    def get_domain(self, url):
        netloc = urlparse(url).netloc
        if netloc.startswith('www.'):
            netloc = netloc[4:]
        return netloc.split('.')[0]

    # check if this parameter written for this domain. Made this for good visual on buttons
    def param_check(self, domain_param):
        return "" if domain_param else " | Default settings"