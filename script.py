import argparse


# Arguments
parser = argparse.ArgumentParser(
    prog="playlink", 
    description="Transforms individual YouTube links into a playlist",
)
parser.add_argument(
    "-l", "--limit", 
    type=int,
    default=50,
    help="current youtube playlist limit (default: 50)",
)
parser.add_argument(
    "-O", "--output", 
    default="output.txt",
    help=".txt output filename (default: 'output.txt')",
)
parser.add_argument(
    "input",
    help="input .txt filename with youtube links",
)

args = parser.parse_args()


# Assigning arguments to variables
playlist_limit = args.limit
input_file = args.input
output_file = args.output if args.output[-4:] == ".txt" else args.output + ".txt"


# Relevant functions
def clean(link):
    for identifier in possible_link_identifiers:
        if identifier in link: 
            start = link.find(identifier) + len(identifier)
            video_id = link[start:start + 11] # YouTube's video IDs are 11 characters long

            return video_id if len(video_id) else "SKIPPING..."

    return "SKIPPING..."


# Global variables
possible_link_identifiers = ["?v=", "&v=", "shorts/", "%3Fv%3D", "youtu.be/", "%26v%3D", "/v/", "embed/", "live/", "/e/", "watch/"]
base_link = "https://www.youtube.com/watch_videos?video_ids="
links = []


count = 0
cur_playlist = []

for line in open(input_file):
    if count < playlist_limit:
        video_id = clean(line)

        if video_id == "SKIPPING...": 
            continue

        cur_playlist.append(video_id)
        count += 1

    else:
        links.append(base_link + ",".join(cur_playlist))

        cur_playlist = []
        count = 0

if cur_playlist:
    links.append(base_link + ",".join(cur_playlist))


with open(output_file, "w") as file:
    for link in links:
        file.write(link + "\n")
