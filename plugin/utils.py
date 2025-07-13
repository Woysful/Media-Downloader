from shlex      import split
from subprocess import run, CalledProcessError
from winsound   import PlaySound, SND_FILENAME
from sys        import exit
from datetime   import datetime
from settings   import Config
from keys       import key_check, url_valid

def logs(config: Config, url: str, query: str, command: list) -> None:
    with open(r".\plugin\logs.txt", "a", encoding="utf-8") as f:
        f.write(
            f"\nTime:\t\t{datetime.now():%d-%m-%Y %H:%M:%S}"
            f"\nDomain:\t\t{config.domain}"
            f"\nLink:\t\t{url}"
            f"\nQuery:\t\t{query}"
            f"\nCommand:\t{command}\n"
        )

def sound_msg(status, config: Config):
    if config.sound:
        sound_file = r'.\sound\done.wav' if status else r'.\sound\warning.wav'
        PlaySound(sound_file, SND_FILENAME)

def win_msg(status, type, config: Config):
    if config.msg:
        match type:
            case "video" | "video_best":
                sub = "Video downloaded successfully!" if status else "Something goes wrong"
            case "audio" | "audio_best":
                sub = "Audio downloaded successfully!" if status else "Something goes wrong"

        from flowlauncher import FlowLauncherAPI
        FlowLauncherAPI.show_msg(
            title="Media Downloader",
            sub_title=sub,
            # ico_path=ico - custom icons doesn't work for some reason ¯\_(ツ)_/¯
        )

# forming yt-dlp command based on button that user pressed
def build_command(button_param: str, url: str, vid_quality: str, config: Config) -> list:
    # if this request has postprocessor arguments
    if config.ff_param:
        return [
            config.ytdlp_path,
            '-f', vid_quality + config.vid_param,
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
                '-f', vid_quality + config.vid_param,
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
def download(button_param, query, config: Config):
    if not url_valid()[0]:
        sound_msg(False, config)
        win_msg(False, button_param, config)
        exit(1)
    else:
        vid_quality, url = key_check(query, config)

        command = build_command(button_param, url, vid_quality, config)
        logs(config, url, query, command)
        try:
            run(command, check=True)
            sound_msg(True, config)
            win_msg(True, button_param, config)
        except CalledProcessError:
            sound_msg(False, config)
            win_msg(False, button_param, config)
            exit(1)