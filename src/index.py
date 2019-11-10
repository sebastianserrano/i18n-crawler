import re
import json
import datetime;
from os import walk, makedirs, path
from os.path import join

ROOT_PATH = "/Users/sebastianserrano/WebstormProjects/shopify-master/app"
DIRTY_JSON_PATH = "test.json"
FINAL_DICTS_PATH = "sanitized-dicts/"

I18N_PREFIX_CALL = "i18n.t"
I18N_REGEX_GROUP_NAME = "chunk"
I18N_REGEX = '.*\{i18n.t\(\"(?P<' + I18N_REGEX_GROUP_NAME + '>.*)\"\)\}'
IGNORE_DIRS = ["node_modules", ".next"]
STRIPPED_CHUNKS = []
JSON_CHUNKS = []
SANITIZED_JSON = {}

def checkI18nExistance(line):
    match = re.match(I18N_REGEX, line)
    return match

def extractChunkFromLine(line):
    return line.group(I18N_REGEX_GROUP_NAME)

def collectChunkInList(list, chunk):
    list.append(chunk)

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

def convertStrippedChunkIntoList(chunk):
    return list(map(lambda s: s.strip(), chunk.split('.')))

def remapLineToDict(line):
    fields = convertStrippedChunkIntoList(line)
    def remapFieldsToDict(fields):
        if (len(fields) > 1):
            callback = remapFieldsToDict(fields[1:])
            return {fields[0]: callback}
        return {fields[0]: fields[0]}

    mappedChunk = remapFieldsToDict(fields)
    collectChunkInList(JSON_CHUNKS, mappedChunk)

def deep_merge_dicts(original, incoming):
    for key in incoming:
        if key in original:
            if isinstance(original[key], dict) and isinstance(incoming[key], dict):
                deep_merge_dicts(original[key], incoming[key])
            else:
                original[key] = incoming[key]
        else:
            original[key] = incoming[key]

def intersectJsons(original, sanitized):
    return {x: original[x] for x in original if x in sanitized}


if __name__ == "__main__":
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

    for chunk in JSON_CHUNKS:
        deep_merge_dicts(SANITIZED_JSON, chunk)

    with open(DIRTY_JSON_PATH, 'r') as json_file:
        dirtyJSON = json.load(json_file)
        intersectedDict = intersectJsons(dirtyJSON, SANITIZED_JSON)
        intersectedDictJson = json.dumps(intersectedDict)
        print(f"{intersectedDictJson}")

    currentDate = str(datetime.datetime.now())
    filename = FINAL_DICTS_PATH + currentDate
    makedirs(path.dirname(filename), exist_ok=True)

    with open(filename, "w") as file:
        file.write(intersectedDictJson)
