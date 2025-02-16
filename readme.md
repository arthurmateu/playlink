# Playlink
Playlink is a CLI tool that generates YouTube playlists from a file.

Please note that since YouTube has a cap for anonymous playlists, the resulting playlists will have at most `LIMIT` (default being 50) videos.

# Usage and options
### Usage
```
python playlink.py [-h] [-O OUTPUT] [--limit LIMIT] [--repeats | --no-repeats] [--auto | --no-auto] [--show | --no-show] [--progress | --no-progress] input
```
### Options
```
positional arguments:
  input                 input `.txt` filename with youtube links

options:
  -h, --help            show this help message and exit
  -O, --output OUTPUT   .txt output filename (default: 'output.txt')
  --limit LIMIT         Video limit per playlist (default: 50 - maximum for YouTube anonymous playlists)
  --repeats, --no-repeats
                        Allows/disallows repeated video (enabled by default)
  --auto, --no-auto     Prints out progress, playlists and opens them automatically (disabled by default)
  --show, --no-show     Outputs playlist link on stdout (disabled by default)
  --progress, --no-progress
                        Shows script progress (disabled by default)
```
