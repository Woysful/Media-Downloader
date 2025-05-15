import sys, os, subprocess, pyperclip, json, tldextract, shlex
ytdlp_path  = '.\plugin\yt-dlp.exe'
ffmpeg_path = '.\plugin\\ffmpeg.exe'

def load_config(config_path="config.json"):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except Exception as e:
        return {} 

def get_domain(url) -> str:
    extracted = tldextract.extract(url)
    domain = extracted.domain
    return domain

def run(param):
    config = load_config()

    output_path     = os.path.join(config.get("Download directory", "%USERPROFILE%\Downloads"), "%(title)s.%(ext)s")    
    vid_format      = config.get("Preferred video format", "mkv")
    aud_format      = config.get("Preferred audio format", "m4a")
    vid_param_def   = config.get("Default video parameters", "bv+ba/best")
    domains_conf    = config.get("domains", {})
    
    url = pyperclip.paste().strip()
    if not url:
        sys.exit(1)
    
    domain          = get_domain(url)
    domain_param    = domains_conf.get(domain, {})
    vid_param       = domain_param.get("yt-dlp parameters", vid_param_def)
    arg_param       = domain_param.get("postprocessor args", "")

    match param:
        case "video":
            command = [ytdlp_path, url, '-o', output_path, '-f', vid_param, '--merge-output-format', vid_format, '--embed-metadata']
        case "video_best":
            command = [ytdlp_path, url, '-o', output_path, '-f', 'bestvideo+bestaudio/best']
        case "audio":
            command = [ytdlp_path, url, '-o', output_path, '-f', 'bestaudio', '-x', '--audio-format', aud_format]
        case "audio_best":
            command = [ytdlp_path, url, '-o', output_path, '-f', 'bestaudio', '-x', '--audio-format', 'wav']
        case _:
            sys.exit(1)

    try:
        if arg_param:
            command = [ytdlp_path,
                       '-f', vid_param,
                       '--merge-output-format', vid_format,                       
                       '--postprocessor-args'] + shlex.split(arg_param) + [
                        '-o', output_path, 
                        '--embed-metadata',
                        url]

            with open("logs.txt", "a", encoding="utf-8") as f:
                f.write("\ndomain: " + domain + "\n")
                f.write("command with args: " + str(command) + "\n\n")

            subprocess.run(command, check=True)
        else:
            with open("logs.txt", "a", encoding="utf-8") as f:
                f.write("domain: " + domain + "\n")
                f.write("command: " + str(command) + "\n\n")

            subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(1)