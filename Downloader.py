import sys
import subprocess
import pyperclip
import json
import os

def load_config(config_path="config.json"):
    # Config read
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"[ Config load error: {e} ]")
        return {}

def main():
    # Parameters check
    if len(sys.argv) != 2:
        print("[ Wrong argument ]")
        sys.exit(1)
    
    mode = sys.argv[1].lower()

    # Config load
    config = load_config()

    # Default settings if config.json isn't exist or has some sort of a problems
    download_directory  = config.get("download_directory", ".")
    video_format        = config.get("preferred_video_format", "mkv")
    audio_output_format = config.get("preferred_audio_format", "m4a")
    video_dwnld_param   = config.get("video download parameters", "bv[vcodec^=hev1]+ba[ext=m4a]/bv[vcodec^=avc1]+ba[ext=m4a]")
    #audio_output_codec  = config.get("preffered_audio_codec", "aac")

    # Getting link from clipboard
    url = pyperclip.paste().strip()
    if not url:
        print("[ No link in clipboard ]")
        sys.exit(1)

    output_template = os.path.join(download_directory, "%(title)s.%(ext)s")

    # yt-dlp commands depends on run parameter
    if mode == "video":
        command = ['yt-dlp', '-f', video_dwnld_param, '-o', output_template, '--remux-video', video_format, '--embed-metadata', url]
    elif mode == "video_best":
        command = ['yt-dlp', '-f', 'bestvideo+bestaudio/best', '-o', output_template, url]
    elif mode == "audio":
        #command = ['yt-dlp', '-f', 'bestaudio', '-x', '--audio-format', audio_output_format, '--postprocessor-args', '-c:a '+audio_output_codec, '-o', output_template, url]
        command = ['yt-dlp', '-f', 'bestaudio', '-x', '--audio-format', audio_output_format, '-o', output_template, url]
    elif mode == "audio_best":
        command = ['yt-dlp', '-f', 'bestaudio', '-x', '--audio-format', 'wav', '-o', output_template, url]
    else:
        print("[ Wrong argument ]")
        sys.exit(1)

    # Running this shit
    print("Running comand:")
    print(" ".join(command))
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("[ ERROR ] yt-dlp:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()