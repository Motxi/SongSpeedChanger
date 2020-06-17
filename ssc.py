import argparse, decimal, time, os, re
from pytube import YouTube
from pydub import AudioSegment

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--download', required=False, action='store_true')
parser.add_argument('-nl', '--no_limit', required=False, action='store_true')
parser.add_argument('-s', '--song', type=str, default=None, required=True)
parser.add_argument('-r', '--rate', type=float, default=1.0, required=False)
parser.add_argument('-e', '--export', type=str, default=os.path.dirname(__file__), required=False)
args = parser.parse_args()


def change_speed(song, export, rate):
    nfr_song = AudioSegment.from_file(song)

    return nfr_song._spawn(
        nfr_song.raw_data,
        overrides={
            'frame_rate': int(nfr_song.frame_rate * rate)
        }
    ).set_frame_rate(nfr_song.frame_rate).export(export, format='mp3')

def handler(function, *args):
    try:
        return function(*args)
    except Exception as e:
        raise Exception(f'Error occurred: {e}')


path = args.export if args.export else os.path.dirname(__file__)
supported_formats = ['.mp4', '.m4a', '.mp3', '.ogg', '.wav', '.wave']
rate = round(args.rate, 2)

if args.download == True:
    # Check if input URL is valid
    song_check = re.match(r'^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})?$', args.song).group()
    
    if song_check:
        # Download video
        video = YouTube(args.song)
        title = video.title

        # Create ./ssc_downloads folder
        folder = f'{os.path.dirname(__file__)}/ssc_downloads'
        if not os.path.isdir(folder):
            os.mkdir(folder)

        time.sleep(1)

        video.streams.filter(
            only_audio=True,
            type='audio'
        ).first().download(
            output_path=folder,
            filename=title
        )

        # Song data
        song_format = '.mp4'
        song_title = re.sub(r'[^\x00-\x7F]+', ' ', video.title)
        # song = f'{os.path.dirname(__file__)}/{song_title}{song_format}'
        song = f'{folder}/{song_title}{song_format}'
        export = f'{path}/({str(rate)}) {song_title}.mp3'
    else:
        raise Exception('Invalid YouTube URL')
else:
    # Check if input path is valid
    song_check = os.path.exists(os.path.dirname(args.song))

    if song_check:
        # Song data
        song_format = re.search(r'\.[^.]*$', os.path.basename(args.song)).group()
        song_title = os.path.basename(args.song)
        song = args.song
        export = f'{path}/({str(rate)}) {song_title.replace(song_format, ".mp3")}'
    else:
        raise Exception('Invalid path')

# Check if input rate is valid
if args.no_limit == False:
    if rate > 2.0 or rate < 0.5:
        raise Exception('Invalid rate (0.5x - 2.0x). Use -nl to remove the rate limit')
elif rate < 0.0:
    raise Exception('why.')

# Check if song format is supported
if song_format not in supported_formats:
    raise Exception(f'Unsupported file format. Please use: {supported_formats}')


if __name__ == '__main__':
    print('Processing...')

    handler(change_speed,song,export,rate)
    end_time = time.time()
    
    # Final info
    print('\n===== Song Speed Changer =====')
    print(f'Song: {os.path.basename(song)}')
    print(f'Rate: {rate}x')
    print(f'Path: {path}')
    print(f'Time: {round(end_time-start_time, 2)}s')
    print('===== Song Speed Changer =====\n')