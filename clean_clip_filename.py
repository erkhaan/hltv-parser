import os
import shutil

player = ''
path = ''
# example: '/Volumes/WD Elements/Videos/Highlights'
target_path = ''

files = os.listdir(path)
for file in files:
    newfile = file.replace(player + ' - ', '')\
        .replace(player + ' ', '')\
        .replace(player + "'s - ", '')\
        .replace(player + "'s'", '')
os.rename(
    os.path.join(path, file),
    os.path.join(path, newfile))

files = os.listdir(path)

target_dir = target_path + '/' + player + '/'
os.makedirs(
    os.path.dirname(target_dir),
    exist_ok=True)
file_names = os.listdir(path)

for file_name in file_names:
    shutil.move(os.path.join(path, file_name), target_dir)
