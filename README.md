## yt-dlp based FlowLauncher plugin
A plugin that allows you to download any (yt-dlp supported services) video/audio files

I'm not a cool coder and made this for myself. But maybe it'll come in handy for you

![](https://github.com/user-attachments/assets/1e47769f-95ee-4481-b449-9300bbdcf379)

## Features
Basically this plugin creates for you 4 respodns:

- **[ Video ]** - Downloading video with configurable parameters and containers. These parameters can be changed in the `config.json`

- **[ Video Best ]**  - Downloading video in best possible quality no matter what codec/container it uses

- **[ Audio ]** - Downloading audio with configurable format. This parameter can be changed in `config.json`

- **[ Audio Best ]** - Downloading audio in best possible quality and converting to `wav`

Also, you don't need to paste the link into the text field. Just copy the link and select the download mode. Plugin takes the link from the clipboard.

## Installation

[Download](https://github.com/Woysful/Media-Downloader/releases/latest/download/Media-Downloader.zip) the archive from the release tab or source code and place the folder from the archive in the folder with other plugins.

The usuall path to the plugin folder is: `%appdata%\FlowLauncher\Plugins\`

## Issues
I didn't figure out how to get user parameters correctly to use yaml document. Unfortunately, to change the settings it is necessary to edit the `config.json` file in the plugin directory.
