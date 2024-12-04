# Playlink
Playlink is a script that generates YouTube playlists from a file.

Since YouTube has a cap for anonymous playlists, your output file will show playlists with at most `LIMIT` (default being 50) videos.

# Usage and options
```
python script.py [OPTIONS] input
```
### General options:
```
  -h, --help                        show this help message and exit
  -l LIMIT, --limit LIMIT           current youtube playlist limit (default: 50)
  -O OUTPUT, --output OUTPUT        .txt output filename (default: 'output.txt')
```
