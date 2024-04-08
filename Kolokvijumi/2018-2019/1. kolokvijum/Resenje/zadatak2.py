import os, re, shutil, zipfile

email_regex = re.compile(r'^[A-Za-z][A-Za-z0-9.-_]{3,}@[a-z]{2,8}\.[a-z]{2,4}$')

file = open('adrese.txt', 'r')
file_ispravne = open('ispravneAdrese.txt', 'w')

for email in file.readlines():
    if email_regex.match(email):
        file_ispravne.write(email)

file.close()
file_ispravne.close()

#os.unlink('adrese.txt')

TEKST = 'TEKST'
XML = 'XMLs'
OSTALO = 'OSTALO'
RAZNO = 'RAZNO'

names = [TEKST, XML, OSTALO]

for name in names:
    if not os.path.exists(name):
        os.mkdir(name)

for path, dirs, files in os.walk(RAZNO):
    for filename in files:
        file_path = os.path.join(path, filename)
        if filename.endswith('.txt'):
            shutil.copy(file_path, TEKST)
        elif filename.endswith('.xml'):
            shutil.copy(file_path, XML)
        else:
            shutil.copy(file_path, OSTALO)

resenje = zipfile.ZipFile('resenje.zip', 'w')

for name in names:
    if name != OSTALO:
        for filename in os.listdir(name):
            file_path = os.path.join(name, filename)
            resenje.write(file_path, compress_type=zipfile.ZIP_DEFLATED)