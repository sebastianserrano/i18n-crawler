import re
import json
from os import walk
from os.path import join

ROOT_PATH = ""
I18N_PREFIX_CALL = "i18n.t"
I18N_GROUP_NAME = "chunk"
I18N_CALL_REGEX = ".*\{i18n.t\(\"(?P<chunk>.*)\"\)\}"
IGNORE_DIRS = ["node_modules", ".next"]
STRIPPED_CHUNKS = []
JSON_CHUNKS = []
SANITIZED_DICT = {}

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
                collectChunkInList(STRIPPED_CHUNKS, chunk)
    except Exception as error:
        print(f"Could not open file at path {fullPath} because {error}")
        pass

def remapLineToDict(line):
    fields = list(map(lambda s: s.strip(), line.split('.')))
    def reduceFields(fields):
        if (len(fields) > 1):
            callback = reduceFields(fields[1:])
            return {fields[0]: callback}
        return {fields[0]: fields[0]}

    mappedChunk = reduceFields(fields)
    JSON_CHUNKS.append(mappedChunk)

for root, dirs, files in walk(ROOT_PATH):
    for item in IGNORE_DIRS:
        if item in dirs:
            dirs.remove(item)
    if len(files) >= 1:
        for file in files:
            openFile(root, file)
    else:
        for file in files:
            openFile(root, file)


for chunk in STRIPPED_CHUNKS:
    mappedLine = remapLineToDict(chunk)

def deep_merge_dicts(original, incoming):
    for key in incoming:
        if key in original:
            if isinstance(original[key], dict) and isinstance(incoming[key], dict):
                deep_merge_dicts(original[key], incoming[key])
            else:
                original[key] = incoming[key]
        else:
            original[key] = incoming[key]

com = {}
for chunk in JSON_CHUNKS:
    deep_merge_dicts(com, chunk)

with open('test.json', 'r') as json_file:
    data = json.load(json_file)
    d = {x: data[x] for x in data if x in com}
    f = json.dumps(d)
    print(f"{f}")
