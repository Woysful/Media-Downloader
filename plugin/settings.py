from os             import path
from json           import load
from urllib.parse   import urlparse

class Config:
    def __init__(self, url):
        current_dir = path.dirname(path.abspath(__file__))
        root_dir    = path.abspath(path.join(current_dir, "..", "..", ".."))

        # settings files path
             # list of domains and their settings
        self.config_path    = r".\plugin\config.json"
            # Flow Launcher plugin user settings
        self.settings_path  = path.join(root_dir, "Settings", "Plugins", "Media Downloader", "settings.json")

        self.ffmpeg_path    = r".\plugin\ffmpeg.exe"
        self.ytdlp_path     = r".\plugin\yt-dlp.exe"
        
        self.config_full    = self.load_json(self.config_path)
        self.settings_full  = self.load_json(self.settings_path)

        self.output_path    = path.join(self.settings_full.get("download_directory", "%USERPROFILE%\\Downloads"), "%(title)s.%(ext)s")
        self.vid_format_def = self.settings_full.get("default_video_format", "mkv")
        self.aud_format_def = self.settings_full.get("default_audio_format", "m4a")
        self.vid_param_def  = self.settings_full.get("default_video_parameters", "bv+ba/best")
        self.sound          = self.settings_full.get("download_complete_sound", True)
        self.msg            = self.settings_full.get("win_msg", True)

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

        domain_param        = self.domains_conf.get(self.domain_work, {})
        self.vid_format     = domain_param.get("video format", self.vid_format_def)
        self.vid_param      = domain_param.get("yt-dlp parameters", self.vid_param_def)
        self.aud_format     = domain_param.get("audio format", self.aud_format_def)
        self.ff_param       = domain_param.get("postprocessor args", "")

        self.vid_param_chk  = self.param_check(domain_param)
        self.aud_param_chk  = self.param_check(domain_param)

        self.ui_format_v    = self.vid_format
        self.ui_format_a    = self.aud_format
        self.ui_quality     = ""
        self.ui_ytdlp       = ""
        self.ui_ffmpeg      = ""
        self.ui_domain      = " | " + self.domain_visual

        # Key lists for query checking
        self.key_list_quality   = ['q', 'Q', 'quality', 'Quality', 'QUALITY']
        self.key_list_format    = ['f' , 'F' , 'format' , 'Format' , 'FORMAT']
        self.key_list_ytdlp     = ['yt' , 'YT' , 'ytdlp' , 'YTDLP' , 'yt-dlp parameters']
        self.key_list_ffmpeg    = ['ff' , 'FF' , 'ffmpeg' , 'FFmpeg' , 'FFMPEG']
        self.key_list_domain    = ['d' , 'D' , 'domain' , 'Domain' , 'DOMAIN']
        self.key_list_settings  = ['s' , 'S' , 'settings' , 'Settings' , 'SETTINGS']
        self.key_list_log       = ['l' , 'L' , 'log' , 'Log' , 'LOG', 'logs', 'Logs', 'LOGS']

    # loads settings from json file
    def load_json(self, path_):
        try:
            with open(path_, "r", encoding="utf-8") as f:
                return load(f)
        except:
            return {}

    # formats and separates the domain for use in the code,
    # as well as combining short and long domains into one, for example youtu.be and youtube.com
    # and visual, for display in the user interface
    def domain_edit(self, domain, rep):
        return rep.get(domain, domain)
    
    # formats the URL and returning only the domain name
    def get_domain(self, url):
        netloc = urlparse(url).netloc
        if netloc.startswith('www.'):
            netloc = netloc[4:]
        return netloc.split('.')[0]

    # checks if there are any individual settings for the domain. Used in the user interface
    def param_check(self, domain_param):
        return "" if domain_param else " | Default settings"