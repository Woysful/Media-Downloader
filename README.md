## yt-dlp based Media Downloader [ Flow Launcher plugin ]
A plugin that allows you to download any (yt-dlp supported services) video/audio files. (windows support only)

I'm not a good programmer and made this for myself. But maybe it'll come in handy for you

![](https://github.com/user-attachments/assets/69a2cce5-21ba-421b-a641-8f4cd417f9b4)

## Features
Basically this plugin creates for you 5 buttons:

- **[ Video ]** - Downloading video with configurable yt-dlp/ffmpeg parameters and containers

- **[ Video Best ]**  - Downloading video in best possible quality no matter what codec/container it uses

- **[ Audio ]** - Downloading audio with configurable format

- **[ Audio Best ]** - Downloading audio in best possible quality and converting to `wav`

- **[ Domain Settings ]** - Opens config.json

The program has two settings files:
The first is a file with settings that the user specifies within Flow Launcher.
These settings include: `download path`, `default video/audio formats`, `default download command`, and the ability to disable `notification sounds`.
`Default format` settings and `download commands` are the settings that are used if the user has not specified individual settings for a particular domain.

Individual settings are specified for each separate domain, if necessary. This can be done in the `config.json` file, which can be opened by selecting `Domain Settings`.
The settings that can be used are described below in the **Config settings** section.

In addition to these settings, the user can also enter the desired format in the query string. This works exclusively with the `Video` and `Audio` items.

Also, you don't need to paste the link into the text field. Just copy the link and select the download mode. Plugin takes the link from the clipboard.

## Installation
[Download](https://github.com/Woysful/Media-Downloader/releases/latest/download/Media-Downloader.zip) the archive from the release tab or source code and place the folder from the archive in the folder with other plugins.

The usuall path to the plugin folder is: `%appdata%\FlowLauncher\Plugins\`

## Config settings
To answer the first question: “why do I need to edit a text file instead of settings inside Flow Launcher?”.
Because I have no idea how to create items list in FL UI plugin settings, I didn't find such an option in the documentation.

### How to use config
To access the file, simply select Settings, which will open it in a text editor.
The file contains default settings and settings for individual domains. The program will use default settings if the domain of link you are trying to download file from does not have unique settings in config.
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
| video format        | The container into which the program will attempt to place the video stream. For example `"mkv"`. Inside the program `--merge-output-format` is used to define the container. Pay close attention to the codec and container compatibility, or use postprocessor args to re-encode video stream |
| audio format        | Audio file format into which the downloaded audio stream will be converted                                                                                                                                                                  |
