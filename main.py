from pytube import YouTube
import subprocess
import shutil
import os

directory = 'audios/'

files = [
    {
    'link' : 'https://youtube.com?v=dr9nRWPzKRo',
    'start' : 0,
    'duration' : 18,
    'name' : 'Toy_Story'
    },
    {
    'link' : 'https://www.youtube.com?v=sb3tHsCLWsI',
    'start' : 111,
    'duration' : 17,
    'name' : 'Man_or_Muppet'
    },
    {
    'link' : 'https://www.youtube.com/watch?v=DeumyOzKqgI',
    'start' : 24,
    'duration' : 20,
    'name' : 'Skyfall'
    },
    {
    'link' : 'https://www.youtube.com/watch?v=MD5bFCDfySc',
    'start' : 6,
    'duration' : 32,
    'name' : 'Frozen'
    },
    {
    'link' : 'https://www.youtube.com/watch?v=Z6BuXRTk5D4',
    'start' : 0,
    'duration' : 24,
    'name' : 'Glory'
    },
    {
    'link' : 'https://www.youtube.com/watch?v=8jzDnsjYv9A',
    'start' : 15,
    'duration' : 29,
    'name' : 'Spectre'
    },
    {
    'link' : 'https://www.youtube.com/watch?v=GTWqwSNQCcg',
    'start' : 74,
    'duration' : 21,
    'name' : 'La_La_Land'
    },
    {
    'link' : 'https://www.youtube.com/watch?v=3iDxU9eNQ_0',
    'start' : 10,
    'duration' : 12,
    'name' : 'Coco'
    },
    {
    'link' : 'https://www.youtube.com/watch?v=bo_efYhYU2A',
    'start' : 65,
    'duration' : 40,
    'name' : 'Shallow'
    },
    {
    'link' : 'https://www.youtube.com/watch?v=0LtusBN3ST0',
    'start' : 16,
    'duration' : 21,
    'name' : 'Rocketman'
    },
]
if not os.path.exists(directory):
    os.makedirs(directory)
f = open(directory + "file.txt","w+")
blank = YouTube('https://www.youtube.com/watch?v=nofYbnd0QMw')
blank.streams.filter(only_audio = True, file_extension = 'mp4').first().download(output_path = directory, filename = 'blank')

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 40, fill = '█', autosize = False):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s' % styling.replace(fill, bar), end = '\r')
    # Print New Line on Complete
    if iteration >= total:
        print()

def download_and_trim_files(links):
    for link in links:
        def progress_function(chunk, file_handle, bytes_remaining):
            size = audio.filesize
            printProgressBar(size - bytes_remaining, size, link['name'])
        
        def on_downloaded(stream, file_handle):
            temp_name = directory + link['name'] + "_temp.mp4"
            command = ["ffmpeg", "-ss", link['start'], "-t", link['duration'], "-i", file_handle, temp_name]
            process = subprocess.Popen(" ".join(str(v) for v in command), shell = True, stdout = None)
            process.wait()
            f.write("file 'blank.mp4'\n")
            f.write("file '" + link['name'] + "_temp.mp4" + "'\n")
        yt = YouTube(link['link'], on_progress_callback = progress_function)
        yt.register_on_complete_callback(on_downloaded)
        audio = yt.streams.filter(only_audio = True, file_extension = 'mp4').first()
        audio.download(output_path = directory, filename = link['name'])

def combine_files():
    result_file = directory + "result.mp4"
    process = subprocess.Popen("ffmpeg -f concat -safe 0 -i " + directory + "file.txt  output.mp4", shell = True, stdout = None)
    process.wait()

download_and_trim_files(files)
f.close()
combine_files()
shutil.rmtree(directory)
