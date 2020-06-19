# song-speed-changer
Automatically change the playback speed of an audio file by providing a YouTube URL or an existing audio file path

## Installation
```bash
pip install -r requirements.txt
```

## Arguments
Argument | Required | Default | Help
--- | --- | --- | ---
-d | No | N/A | Download YouTube video (AudioOnly)
-nl | No | N/A | Removes rate limit
-s | Yes | None | Audio file path (YouTube URL if **-d** is enabled)
-r | No | 1.0 | Playback speed rate
-e | No | CWD | Export path

**Note:** When downloading a video from YouTube using **-d**, the raw AudioOnly file will be downloaded to a **ssc_downloads** folder that will be created in the current directory. You can either save the raw file or delete it.

## Example 1
Download a YouTube song, set playback speed to 1.4x and export it to the desktop
```bash
ssc.py -d -s "https://www.youtube.com/watch?v=elfawRZX1t0" -r 1.4 -e "C:\Users\~\Desktop"
```

## Example 2
Set playback speed of an existing audio file to 3.0x and export it to the current directory
```bash
ssc.py -nl -s "C:\Users\~\Music\song.mp3" -r 3.0
```