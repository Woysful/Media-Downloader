from shlex      import split
from subprocess import run, CalledProcessError
from winsound   import PlaySound, SND_FILENAME
from sys        import exit
from os         import startfile
from re         import finditer
from datetime   import datetime
from settings   import Cfg

# notification sound
def sound_msg(status, config: Cfg):
    if config.sound == True:
        match status:
            case True:        
                PlaySound(r'.\sound\done.wav', SND_FILENAME)
            case False:
                PlaySound(r'.\sound\warning.wav', SND_FILENAME)                

# parsing keys from query field
def query_keys(query, config: Cfg):
    pattern = r'-(\w+)(?:\s+([^-\s][^-]*))?'

    args = {}
    for match in finditer(pattern, query):
        key = match.group(1)
        value = match.group(2).strip() if match.group(2) else None
        args[key] = value

    if query.replace(" ", "") != "":
        for key, value in args.items():
            match key:
                case 'f':
                    config.vid_format = config.aud_format = args.get('f')
                case 'yt':
                    config.vid_param  = args.get('yt')
                case 'ff':
                    config.ff_param   = args.get('ff')
                case 'd':
                    startfile(config.config_path)
                    exit(1)
                case 's':
                    startfile(config.settings_path)
                    exit(1)
                case _:
                    sound_msg(False, config)

# running the whole thing
def run_d(param, query, config: Cfg):
    if (not config.url) or (not config.url_pattern.match(config.url)):
        sound_msg(False, config)
    else:
        query_keys(query, config)

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
                exit(1)

        # if this domain has postprocessor arguments in config
        try:
            if config.ff_param:
                command = [config.ytdlp_path,
                        '-f', config.vid_param,
                        '--merge-output-format', config.vid_format,                       
                        '--postprocessor-args'] + split(config.ff_param) + [
                            '-o', config.output_path, 
                            '--embed-metadata',
                            config.url]

                with open(".\plugin\logs.txt", "a", encoding="utf-8") as f:
                    f.write("\nTime: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                    f.write("\nDomain: " + config.domain)
                    f.write("\nLink: " + config.url)
                    f.write("\nQuery: " + query)
                    f.write("\nCommand with args: " + str(command) + "\n")

                run(command, check=True)
                if config.sound == True:
                    sound_msg(True, config)
            else:
                with open(".\plugin\logs.txt", "a", encoding="utf-8") as f:
                    f.write("\nTime: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                    f.write("\nDomain: " + config.domain)
                    f.write("\nLink: " + config.url)
                    f.write("\nQuery: " + query)
                    f.write("\nCommand: " + str(command) + "\n")

                run(command, check=True)
                if config.sound == True:
                    sound_msg(True, config)
        except CalledProcessError as e:
            if config.sound == True:
                sound_msg(False, config)
            exit(1)