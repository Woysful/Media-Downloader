import sys, os, subprocess, pyperclip, json

def load_config(config_path="config.json"):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except Exception as e:
        return {}

def run(mode):

    config = load_config()

    download_directory  = config.get("download_directory", ".")
    video_format        = config.get("preferred_video_format", "mkv")
    audio_output_format = config.get("preferred_audio_format", "m4a")
    video_dwnld_param   = config.get("video download parameters", "bv[vcodec^=hev1]+ba[ext=m4a]/bv[vcodec^=avc1]+ba[ext=m4a]")
    
    url = pyperclip.paste().strip()
    if not url:
        sys.exit(1)

    ytdlp_path      = '.\plugin\yt-dlp.exe'
    output_template = os.path.join(download_directory, "%(title)s.%(ext)s")

    match mode:
        case "video":
            command = [ytdlp_path, '-f', video_dwnld_param, '-o', output_template, '--remux-video', video_format, '--embed-metadata', url]
        case "video_best":
            command = [ytdlp_path, '-f', 'bestvideo+bestaudio/best', '-o', output_template, url]
        case "audio":
            command = [ytdlp_path, '-f', 'bestaudio', '-x', '--audio-format', audio_output_format, '-o', output_template, url]
        case "audio_best":
            command = [ytdlp_path, '-f', 'bestaudio', '-x', '--audio-format', 'wav', '-o', output_template, url]
        case _:
            sys.exit(1)

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(1)