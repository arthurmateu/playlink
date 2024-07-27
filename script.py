import argparse


#args
parser = argparse.ArgumentParser(prog="playlink", description="Transforms individual YouTube links into a playlist")
parser.add_argument(
    "-l", "--limit", 
    type=int,
    default=50,
    help="current youtube playlist limit (default: 50)")
parser.add_argument(
    "-O", "--output", 
    default="output.txt",
    help=".txt output filename (default: 'output.txt')")
parser.add_argument(
    "input",
    help="input .txt filename with youtube links")
args = parser.parse_args()


#variables
playlist_limit = args.limit
base_link = "https://www.youtube.com/watch_videos?video_ids="
input_file = args.input
output_file = args.output if args.output[-4:] == '.txt' else args.output + '.txt'
links = []
possible_link_identifiers = ['?v=', '&v=', 'shorts/', '%3Fv%3D', 'youtu.be/', '%26v%3D', '/v/', 'embed/', 'live/', '/e/', 'watch/']


#actual script
def clean(link):
    for identifier in possible_link_identifiers:
        if identifier in link: 
            start = len(identifier) + link.find(identifier)
            video_id = link[start:start+11]
            return video_id if len(video_id) else 'SKIPPING...'
    return 'SKIPPING...'


with open(input_file) as file:
    cur_playlist, count = base_link, 0
    for line in file:
        if count < playlist_limit:
            video_id = clean(line)
            if video_id == 'SKIPPING...': continue
            cur_playlist += video_id + ','
            count += 1
        else:
            links.append(cur_playlist[:-1])
            cur_playlist, count = base_link, 0
    links.append(cur_playlist[:-1])


with open(output_file, 'w') as file:
    for link in links:
        file.write(link + "\n")
