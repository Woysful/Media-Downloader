import os, requests, zipfile, io

ffmpeg_url  = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
ffmpeg_path = r'.\plugin\ffmpeg.exe'

ytdlp_url  = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
ytdlp_path = r'.\plugin\yt-dlp.exe'

working_dir  = '.\plugin'

async def install_ffmpeg():
    if not os.path.isfile(ffmpeg_path):
        response = requests.get(ffmpeg_url)
        response.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            ffmpeg_in_zip = None
            for file_info in z.infolist():
                if file_info.filename.endswith('bin/ffmpeg.exe'):
                    ffmpeg_in_zip = file_info.filename
                    break
            
            os.makedirs(working_dir, exist_ok=True)
            
            with z.open(ffmpeg_in_zip) as ffmpeg_file, open(ffmpeg_path, 'wb') as out_file:
                out_file.write(ffmpeg_file.read())
    return True
      
async def install_ytdlp():
    if not os.path.isfile(ytdlp_path):
        response = requests.get(ytdlp_url)
        response.raise_for_status()
        os.makedirs(working_dir, exist_ok=True)
        with open(ytdlp_path, 'wb') as f:
            f.write(response.content)
    return True

# if __name__ == "__main__":
#     print("\n\n")
#     print("Downloading yt-dlp...")
#     install_ytdlp()
#     print("Downloading ffmpeg...")
#     install_ffmpeg()
#     print("\nComplete!")
#     print("\nYou can now close this window and continue using the plugin")
#     print("\nHave a great day :3")