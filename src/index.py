import re
import json
from os import walk
from os.path import join

I18N_PREFIX_CALL = "i18n.t"
I18N_GROUP_NAME = "chunk"
I18N_CALL_REGEX = ".*\{i18n.t\(\"(?P<chunk>.*)\"\)\}"
IGNORE_DIRS = ["node_modules", ".next"]
CHUNKS = []

def collectChunkInList(list, chunk):
    list.append(chunk)

def checkI18nExistance(line):
    match = re.match(I18N_CALL_REGEX, line)
    return match

def extractChunkFromLine(line):
    return line.group("chunk")

def openFile(root, file):
    fullPath = join(root, file)

    try:
        for line in open(fullPath, "r"):
            result = checkI18nExistance(line)
            if result:
                chunk = extractChunkFromLine(result)
                collectChunkInList(CHUNKS, chunk)
    except Exception as error:
        print(f"Could not open file at path {fullPath} because {error}")

for root, dirs, files in walk("target"):
    for item in IGNORE_DIRS:
        if item in dirs:
            dirs.remove(item)
    if len(files) >= 1:
        for file in files:
            openFile(root, file)
    else:
        for file in files:
            openFile(root, file)

print("\nThese are my chunks ", CHUNKS)
