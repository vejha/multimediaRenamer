import exifread
import pyexifinfo #exiftool required
import os
import glob
import time
import sys

src_dir = sys.argv[1]

if src_dir:
    os.chdir(src_dir)
else:
    try:
        os.chdir(os.path.dirname(__file__))
        src_dir = os.path.dirname(__file__)
    except:
        pass
    

ext_dict = {'images': ['*.JPG', '*.jpg'], 'videos': ['*.MP4', '*.mp4']}

for file_type in ext_dict.keys():
    fileList = []
    for ext in ext_dict[file_type]:
        fileList.extend(glob.glob(src_dir + ext))

    for fileName in fileList:
        try:
            with open(fileName, 'rb') as f:
                if file_type == 'images':
                    tags = exifread.process_file(f)
                    date_str = tags['EXIF DateTimeOriginal']
                else:
                    media_info = pyexifinfo.information(fileName)
                    date_str = media_info['QuickTime:CreateDate']

            fileTime_obj = time.strptime(str(date_str), '%Y:%m:%d %H:%M:%S')
            fileTime_formatted = time.strftime('%Y-%m-%d_%H-%M-%S', fileTime_obj)

            newFileName = fileTime_formatted + ext_dict[file_type][-1][1:]
            os.rename(fileName, newFileName)
            print(fileName + " >> " + newFileName)
        except:
            print("No EXIF tag found...")
            pass
