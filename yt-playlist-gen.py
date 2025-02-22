import argparse
import webbrowser


# Arguments
parser = argparse.ArgumentParser(
    prog="yt-playlist-gen",
    description="Transforms individual YouTube links into a playlist",
)
parser.add_argument(
    "input",
    help="input `.txt` filename with youtube links",
)
parser.add_argument(
    "-O",
    "--output",
    default="output.txt",
    help=".txt output filename (default: 'output.txt')",
)
parser.add_argument(
    "--limit",
    type=int,
    default=50,
    help="Video limit per playlist (default: 50 - maximum for YouTube anonymous playlists)",
)
parser.add_argument(
    "--repeats",
    default=True,
    help="Allows/disallows repeated video (enabled by default)",
    action=argparse.BooleanOptionalAction,
)
parser.add_argument(
    "--auto",
    default=False,
    help="Prints out progress, playlists and opens them automatically (disabled by default)",
    action=argparse.BooleanOptionalAction,
)
parser.add_argument(
    "--show",
    default=False,
    help="Outputs playlist link on stdout (disabled by default)",
    action=argparse.BooleanOptionalAction,
)
parser.add_argument(
    "--progress",
    default=False,
    help="Shows script progress (disabled by default)",
    action=argparse.BooleanOptionalAction,
)

args = parser.parse_args()


# Assigning arguments to variables
playlist_limit = args.limit
input_file = args.input
output_file = args.output if args.output[-4:] == ".txt" else args.output + ".txt"
repeats = args.repeats
auto = args.auto
show_stdout = args.show or args.auto
show_progress = args.progress or args.auto


# Relevant functions
def clean(link):
    for identifier in possible_link_identifiers:
        if identifier in link:
            start = link.find(identifier) + len(identifier)
            video_id = link[
                start : start + 11
            ]  # YouTube's video IDs are 11 characters long

            return video_id if len(video_id) else "INVALID-ID"

    return "INVALID-ID"


def separate(video_ids):
    links = []

    for i in range(0, len(video_ids), playlist_limit):
        batch = video_ids[i : i + playlist_limit]
        cur_playlist = base_link + ",".join(batch)

        links.append(cur_playlist)

    return links


def progress(message):
    if show_progress:
        print(message)


# Global variables
possible_link_identifiers = [
    "?v=",
    "&v=",
    "shorts/",
    "%3Fv%3D",
    "youtu.be/",
    "%26v%3D",
    "/v/",
    "embed/",
    "live/",
    "/e/",
    "watch/",
]
base_link = "https://www.youtube.com/watch_videos?video_ids="

# Tried having just a video_ids variable but my editor was giving me a ton of errors.
# I don't like the color red so I just opted for this compromise.
u_video_ids = set()
video_ids = []


# Actual script begins here
progress("# Fetching IDs from input file...")

for line in open(input_file):
    video_id = clean(line)

    if video_ids == "INVALID-ID":
        continue

    if not repeats:
        u_video_ids.add(video_id)
    else:
        video_ids.append(video_id)


progress("# Turning IDs into playlist(s)...")

if not repeats:
    links = separate(list(u_video_ids))
else:
    links = separate(video_ids)


progress("# Creating an output file with playlist(s)...")

with open(output_file, "w") as file:
    for link in links:
        file.write(link + "\n")


# Small hack I had to look up:
# \033[F --> Moves cursor up
# \r --> Resets cursor to start of the line
# \033[K --> Clears to end of the line
if show_stdout:
    print("# Playlist links:\n")

    for link in links:
        print(f"\033[F\r\033[K{link}", end="\n\n")

        if auto:
            webbrowser.open_new_tab(link)

            pause = input("\033[F\r\033[KContinue? [Y/n] - ").upper()
            if pause and pause[0] == "N":
                print("\033[F\r\033[K^ Last accessed playlist ^", end="\n\n")
                auto = False

    print("\033[F\r\033[K", end="")  # Clean up last empty line
