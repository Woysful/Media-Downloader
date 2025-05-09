## yt-dlp based FlowLauncher plugin
A plugin that allows you to download any (yt-dlp supported services) video/audio files

I'm not a cool coder and made this for myself. But maybe it'll come in handy for you

![](https://github.com/user-attachments/assets/94e6bd34-a6ea-4f0c-ac98-719dffc3d1f2)

## Features
Basically this plugin creates for you 4 respodns:

- **[ Video ]** - Downloading video with configurable parameters and containers. These parameters can be changed in the `config.json`

- **[ Video Best ]**  - Downloading video in best possible quality no matter what codec/container it uses

- **[ Audio ]** - Downloading audio with configurable format. This parameter can be changed in `config.json`

- **[ Audio Best ]** - Downloading audio in best possible quality and converting to `wav`

Also, you don't need to paste the link into the text field. Just copy the link and select the download mode. Plugin takes the link from the clipboard.

## Installation

Download the source code or archive from the release tab and put the folder from the archive in the folder with the other plugins.

The usuall path to the plugins is:
``
%appdata%\FlowLauncher\Plugins\
``

## Issues
I didn't figure out how to get user parameters correctly to use yaml document. Unfortunately, to change the settings it is necessary to edit the `config.json` file in the plugin directory.
