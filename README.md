## yt-dlp based FlowLauncher plugin
A plugin that allows you to download any (yt-dlp supported services) video/audio files
I'm not a cool coder and made this for myself. But maybe it'll come in handy for you

![](https://private-user-images.githubusercontent.com/50032205/441913861-1979d942-7017-4825-9969-c5c630c08edc.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDY3NDY3ODcsIm5iZiI6MTc0Njc0NjQ4NywicGF0aCI6Ii81MDAzMjIwNS80NDE5MTM4NjEtMTk3OWQ5NDItNzAxNy00ODI1LTk5NjktYzVjNjMwYzA4ZWRjLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA1MDglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwNTA4VDIzMjEyN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTY1NWY3OTJhZDRmNDFjNjc5ZGIwNDdkOGMyMDU4Nzg0OWEzZjFjMGZkNjMxYjc3N2QxYTA2ZGQzOWM5MzJjNWYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.XbslgcGhP_NShWD-iv9uEdWISulM5ZTwGRrNC20nGoc)

### Features
Basically this plugin creates for you 4 respodns:

- **[ Video ]** - Downloading video with configurable parameters and containers. These parameters can be changed in the `config.json`

- **[ Video Best ]**  - Downloading video in best possible quality no matter what codec/container it uses

- **[ Audio ]** - Downloading audio with configurable format. This parameter can be changed in `config.json`

- **[ Audio Best ]** - Downloading audio in best possible quality and converting to `wav`

Also, you don't need to paste the link into the text field. Just copy the link and select the download mode. Plugin takes the link from the clipboard.

### Installation

Download the source code or archive from the release tab and put the folder from the archive in the folder with the other plugins.

The usuall path to the plugins is:
``
%appdata%\FlowLauncher\Plugins\
``

### Issues
I have no way to realize the work with plugin settings using yaml document. Unfortunately, to change the settings it is necessary to edit the `config.json` file in the plugin directory.
