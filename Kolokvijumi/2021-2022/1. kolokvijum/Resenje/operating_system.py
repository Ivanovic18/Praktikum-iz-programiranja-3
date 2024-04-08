import os, re, shutil, send2trash, zipfile
 
def move_files(OPERATING_SYSTEM_LOGS, CORE_DUMP_FOLDER, regex):
    if not os.path.exists(CORE_DUMP_FOLDER):
        os.mkdir(CORE_DUMP_FOLDER)

    for path, dirs, files in os.walk(OPERATING_SYSTEM_LOGS):
        for filename in files:
            file_path = os.path.join(path, filename)
            if regex.match(filename) and 15 <= len(filename) <= 30:
                shutil.move(file_path, CORE_DUMP_FOLDER)
            else:
                os.unlink(file_path)

def zip_files(path):
    with zipfile.ZipFile('core_dump.zip', 'w') as zip_file:
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            zip_file.write(file_path, filename, compress_type=zipfile.ZIP_DEFLATED)


def delete_files(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        send2trash.send2trash(file_path)

def get_sizes(path, FILES):
    file = open(path, 'r')
    files = open(FILES, 'a')
    dictionary = {}

    for line in file.readlines():
        filename, disk, size = line.split(',')
        files.write(filename + '\n')
        size = int(size)
        dictionary[disk] = dictionary.get(disk, 0) + size
    
    file.close()
    files.close()
    return dictionary

OPERATING_SYSTEM_LOGS = 'operating_system_logs'
FILE_SYSTEM = 'file_system'
CORE_DUMP_FOLDER = 'core_dump_folder'
DISK_USAGE = 'disk_sizes.txt'
FILES = 'files.txt'

regex = re.compile(r'^[A-Z0-9][a-z@#$_]*\.core_dump$')

move_files(OPERATING_SYSTEM_LOGS, CORE_DUMP_FOLDER, regex)
zip_files(CORE_DUMP_FOLDER)
delete_files(CORE_DUMP_FOLDER)

dictionary = {}
file = open(FILES, 'w')
file.close()

for filename in os.listdir(FILE_SYSTEM):
    if filename.endswith('.txt'):
        file_path = os.path.join(FILE_SYSTEM, filename)
        sizes_dictionary = get_sizes(file_path, FILES)
        for disk, size in sizes_dictionary.items():
            dictionary[disk] = dictionary.get(disk, 0) + size

with open(DISK_USAGE, 'w') as file:
    for disk, size in dictionary.items():
        file.write(f'{disk},{size}\n')
