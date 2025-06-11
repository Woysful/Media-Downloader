from shlex      import split
from subprocess import run, CalledProcessError
from winsound   import PlaySound, SND_FILENAME
from sys        import exit
from datetime   import datetime
from settings   import Cfg
from keys       import key_check, url_valid

# logs for a few things
def logs(config: Cfg, url: str, query: str, command: list) -> None:
    with open(r".\plugin\logs.txt", "a", encoding="utf-8") as f:
        f.write(
            f"\nTime:\t\t{datetime.now():%d-%m-%Y %H:%M:%S}"
            f"\nDomain:\t\t{config.domain}"
            f"\nLink:\t\t{url}"
            f"\nQuery:\t\t{query}"
            f"\nCommand:\t{command}\n"
        )

# notification sound
def sound_msg(status, config: Cfg):
    if config.sound:
        sound_file = r'.\sound\done.wav' if status else r'.\sound\warning.wav'
        PlaySound(sound_file, SND_FILENAME)              

# forming yt-dlp command based on button that user pressed
def build_command(button_param: str, url: str, config: Cfg) -> list:
    # if this request has postprocessor arguments
    if config.ff_param:
        return [
            config.ytdlp_path,
            '-f', config.vid_param,
            '--merge-output-format', config.vid_format,
            '--postprocessor-args', *split(config.ff_param),
            '-o', config.output_path,
            '--embed-metadata',
            url
        ]
    match button_param:
        case "video":
            return [
                config.ytdlp_path, url,
                '-o', config.output_path,
                '-f', config.vid_param,
                '--merge-output-format', config.vid_format,
                '--embed-metadata'
            ]
        case "video_best":
            return [
                config.ytdlp_path, url,
                '-o', config.output_path,
                '-f', 'bestvideo+bestaudio/best'
            ]
        case "audio":
            return [
                config.ytdlp_path, url,
                '-o', config.output_path,
                '-f', 'bestaudio',
                '-x', '--audio-format', config.aud_format
            ]
        case "audio_best":
            return [
                config.ytdlp_path, url,
                '-o', config.output_path,
                '-f', 'bestaudio',
                '-x', '--audio-format', 'wav'
            ]
        case _:
            exit(1)

# running the whole thing
def run_d(button_param, query, config: Cfg):
    if not url_valid()[0]:
        sound_msg(False, config)
        exit(1)
    else:
        # getting params from keys
        keys, url = key_check(query)
        if query.replace(" ", "") != "":
            for key, value in keys.items():
                match key:
                    case 'f':
                        config.vid_format = config.aud_format = keys.get("f", config.vid_format)
                    case 'yt':
                        config.vid_param = keys.get("yt", config.vid_param)
                    case 'ff':
                        config.ff_param = keys.get("ff", config.vid_param)

        command = build_command(button_param, url, config)
        logs(config, url, query, command)
        try:
            run(command, check=True)
            sound_msg(True, config)
        except CalledProcessError:
            sound_msg(False, config)
            exit(1)