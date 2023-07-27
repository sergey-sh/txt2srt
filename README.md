# txt2srt.py utility for convert transcribed text to SubRip format

For show subtitles in video players like vlc or other format like
```text
MM:SS
Text Text Text 

```

does not show but the SubRip format like:

```text
1
HH:MM:SS.MS --> HH:MM:SS.MS 
Text
Text 
Text
```

seen without problem

# Examples

I am use this utility for convert transcribed text from Slack to SubRip format.

Example:
```bash
python txt2srt.py video1863851528.txt video1863851528.srt 80

```

File video1863851528.txt:
```text
00:00
Some Text talk in video

00:30
Continue talk
```

And result Out file video1863851528.srt
```text
00:00:00.000 --> 00:00:30.000 
Some Text talk in video

00:00:30.000 --> 00:05:30.000
Continue talk


```

