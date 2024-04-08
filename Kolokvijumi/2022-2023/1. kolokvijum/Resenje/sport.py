import re, os, shutil, send2trash, zipfile

def move_files(ALL_DATA, TRANSFERS, regex):
    if not os.path.exists(TRANSFERS):
        os.mkdir(TRANSFERS)

    for path, dirs, files in os.walk(ALL_DATA):
        for filename in files:
            file_path = os.path.join(path, filename)
            if regex.match(filename) and 20 <= len(filename) <= 30:
                shutil.move(file_path, TRANSFERS)
            elif filename.endswith('.xml'):
                send2trash.send2trash(file_path)
            else:
                os.unlink(file_path)

def load(path):
    dictionary = {}
    file = open(path, 'r')
    
    for line in file.readlines():
        player_id, team_id = map(int, line.split(','))
        dictionary[player_id] = team_id

    file.close()

    return dictionary

ALL_DATA = 'all_data'
TRANSFERS = 'transfers'
PLAYERS_TEAMS = 'players-teams.txt'
PLAYERS_TEAMS_FINAL = 'players-teams-final.txt'

regex = re.compile('\d{4}-\d{2}-\d{2}_[A-Za-z-_]*.trans(fer)?$')

move_files(ALL_DATA, TRANSFERS, regex)

dictionary = load(PLAYERS_TEAMS)

for filename in os.listdir(TRANSFERS):
    file_path = os.path.join(TRANSFERS, filename)
    transfer_dict = load(file_path)
    for player_id, team_id in transfer_dict.items():
        dictionary[player_id] = team_id

file = open(PLAYERS_TEAMS_FINAL, 'w')

for player_id, team_id in dictionary.items():
    file.write(f'{player_id},{team_id}\n')

file.close()

with zipfile.ZipFile('transfers.zip', 'w') as zip_file:
    for filename in os.listdir(TRANSFERS):
        file_path = os.path.join(TRANSFERS, filename)
        zip_file.write(file_path, filename, compress_type=zipfile.ZIP_DEFLATED)
    zip_file.write(PLAYERS_TEAMS_FINAL, compress_type=zipfile.ZIP_DEFLATED)
