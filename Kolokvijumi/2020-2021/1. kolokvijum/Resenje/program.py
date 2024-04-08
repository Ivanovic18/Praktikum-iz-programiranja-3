import os, re, shutil, send2trash, zipfile

def calculate_points(path):
    file = open(path, 'r')
    counter = 0
    counter2 = 0
    for line in file.readlines():
        points, success = map(int, line.split())
        if(success):
            counter += points
            counter2 += points
        else:
            counter -= points // 2

    return counter, counter2

regex = re.compile(r'^[A-Z][A-Za-z0-9]*@IMI$')

for dir in os.listdir():
    if os.path.isdir(dir):
        recnik = {}
        os.chdir(dir)
        file = open(f'{dir}.txt', 'w')
        file2 = open(f'{dir}.dat', 'w')
        os.chdir('..')
        for team in os.listdir(dir):
            team_path = os.path.join(dir, team)
            if os.path.isdir(team_path):
                if not(regex.match(team) and 7 <= len(team) <= 12):
                    exit(f'Imena timova iz utakmice {dir} krse pravila IMI lige')
                else:
                    final_score = 0
                    for player_file in os.listdir(team_path):
                        player_file_path = os.path.join(team_path, player_file)
                        
                        if player_file.endswith('.txt'):
                            player_name = player_file.split('.txt')[0]
                            player_points, success_actions = calculate_points(player_file_path)
                            recnik[player_name] = player_points
                            final_score += success_actions
                            file.write(f'{player_name} - {team} - {recnik[player_name]}\n')
                        else:
                            os.unlink(player_file_path)
                    file2.write(f'{team}: {final_score}\n')
        file.close()
        file2.close()
        
        os.chdir(dir)
        zip_file = zipfile.ZipFile('statistika.zip', 'w')
        zip_file.write(f'{dir}.txt', compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write(f'{dir}.dat', compress_type=zipfile.ZIP_DEFLATED)
        zip_file.close()
        os.unlink(f'{dir}.txt')
        os.unlink(f'{dir}.dat')
        os.chdir('..')