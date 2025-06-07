# yt-dlp based Media Downloader [ Flow Launcher plugin ]
A plugin that allows you to download any (yt-dlp supported services) video/audio files. (windows support only)

I'm not a good programmer and made this for myself. But maybe it'll come in handy for you

![](https://github.com/user-attachments/assets/46fde6e2-6898-48e6-9513-31f4e1629c1d)

## Features

- Downloading Video/Audio with customizable yt-dlp parameters
- Customized download settings for individual domains
- Temporal downloading parameters
- ffmpeg postprocessor arguments customization
- Link takes from clipboard

# Installation
[Download](https://github.com/Woysful/Media-Downloader/releases/latest/download/Media-Downloader.zip) the archive from the release tab or source code and place the folder from the archive in the folder with other plugins.

The usuall path to the plugin folder is: `%appdata%\FlowLauncher\Plugins\`

## Details and how to use
### Main responds
Basically this plugin creates for you 5 buttons:

- `Video` - Downloading video with configurable yt-dlp/ffmpeg parameters and containers

- `Video Best`  - Downloading video in best possible quality no matter what codec/container it uses

- `Audio` - Downloading audio with configurable format

- `Audio Best` - Downloading audio in best possible quality and converting to `wav`

- `Domain Settings` - Opens config.json

### Global Settings
This plugin has two settings files:
The first is a file with settings that the user specifies within Flow Launcher.
These settings include:
- `download path`

- `default video/audio formats`

- `default yt-dlp download command`

- `notification sounds` switch

`Default` are the settings that are used if the user _**has not**_ specified individual settings for a particular domain. This means that these are global settings for anything that is not uniquely customized.

### Individual Settings
Individual settings are specified for each separate domain, if user wants to. This can be done in the `config.json` file, which can be opened by selecting `Domain Settings` respond, or using `-d` key in the query field.

To answer the first question: “why do I need to edit a text file instead of settings inside Flow Launcher?”.
Because I have no idea how to create items list in FL UI plugin settings.

The structure of domain settings is as follows:
```
...
  "domains" : {
    "domain name"   : {
      "parameter 1"  : "parameters",
      "parameter 2"  : "parameters",
      "parameter n"  : "parameters"
    },
...
```
### List of available parameters:
| Parameter           | Description                                                                                                                                                                                                                                 |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| yt-dlp parameters   | yt-dlp download parameters that come after the `-f` key. For example `"bestvideo+bestaudio/best"`                                                                                                                                           |
| postprocessor args  | Parameters that are passed to ffmpeg. For example `"'-c:v libx265 -c:a aac '"`. **Warning!** It is strictly necessary to specify parameters in double and single quotes as in the example.                                                  |
| video format        | The container into which the program will attempt to place the video stream.For example `"mkv"`. Inside the program `--merge-output-format` is used to define the container. Pay close attention to the codec and container compatibility, or use postprocessor args to re-encode video stream |
| audio format        | Audio file format into which the downloaded audio stream will be converted                                                                                                                                                                  |

## Keys and temporal parameters
Using various keys, user can temporarily change the download settings.
This is useful in situations where it is necessary to download a video/audio file in a format and with settings that do not match the global or individual settings.
Keys can be used so that the user does not have to change the settings in text files just to download a single file.

| key  | Description                              | Example                 |
|:-----|:-----------------------------------------|:------------------------|
|`-f`  | video/audio format                       | mp4                     |
|`-yt` | yt-dlp parameters                        | bv+ba/best              |
|`-ff` | ffmpeg postprocessor arguments           | '-c:v libx265 -c:a aac '|
|`-d`  | Opens Domain Settings file `config.json` |                         |
|`-s`  | Opens User Settings file `settings.json` |                         |

User can find help list with all keys and domain parameters in context menu that can be found by pressing any of this:
- `shift` + `enter`
- `right arrow key`
- `right mouse button` on any respond

Also user does not need to paste the link to his video/audio in the query field. It is enough to have it in the clipboard, from where the program will take the link for downloading.
