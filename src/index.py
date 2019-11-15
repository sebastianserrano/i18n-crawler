"""
    Main entrypoint.

    1. Traverse ROOT_PATH recursively to find all occurrences of the i18n.t() call
    2. Extract 'settings.account.dummy' from i18.t('settings.account.dummy')
    3. Convert 'settings.account.dummy' to {settings: {account: {dummy: dummy }}}
    4. Convert single dicts into a global sanitized dict with deep_merge_dicts
    5. Intersect sanitized global dict with dirty dict from translations.js replacing leaves along the way
    6. Save final sanitized global output to file under sanitized-dicts for later extraction
    7. Output will be a valid Javascript object that can be injected into the translation tool
"""

import re
import json
import datetime
from os import walk, makedirs, path
from os.path import join

ROOT_PATH = "/Users/sebastianserrano/WebstormProjects/shopify-master/app"
DIRTY_JSON_PATH = "test.json"
FINAL_DICTS_PATH = "sanitized-dicts/"

I18N_PREFIX_CALL = "i18n.t"
I18N_REGEX_GROUP_NAME = "chunk"
I18N_REGEX = r".*i18n.t\(\"\b(?P<" + I18N_REGEX_GROUP_NAME + r">.*)\b\".*\)"
IGNORE_DIRS = ["node_modules", ".next"]
STRIPPED_CHUNKS = []
JSON_CHUNKS = []
SANITIZED_JSON = {}
ERROR_FILENAMES = []


def checkI18nExistance(line):
    """ Check if line is calling i18n """
    match = re.match(I18N_REGEX, line)
    return match


def extractChunkFromLine(line):
    """ Extract string(path) from i18n call """
    return line.group(I18N_REGEX_GROUP_NAME)


def collectChunkInList(array, chunk):
    """ Append chunk to param list """
    array.append(chunk)


def openFile(root, file):
    """ Open file and look for i18n call on every line """
    fullPath = join(root, file)

    try:
        for line in open(fullPath, "r"):
            result = checkI18nExistance(line)
            if result:
                chunk = extractChunkFromLine(result)
                collectChunkInList(STRIPPED_CHUNKS, chunk)
    except:
        collectChunkInList(ERROR_FILENAMES, file)


def convertStrippedChunkIntoList(chunk):
    """ Convert editProduct.genre.error to [editProduct, genre, error] """
    return list(map(lambda s: s.strip(), chunk.split('.')))


def remapLineToDict(line):
    """ Convert 'editProduct.genre.error' to {editProduct: {genre: {error: error}}} """
    fields = convertStrippedChunkIntoList(line)

    def remapFieldsToDict(fields):
        """ Convert editProduct.genre.error recursively to {editProduct: {genre: {error: error}}}
            In order to reconstruct true dict skeleton. Leaf value will be replaced after
        """
        if len(fields) > 1:
            callback = remapFieldsToDict(fields[1:])
            return {fields[0]: callback}
        return {fields[0]: fields[0]}

    mappedChunk = remapFieldsToDict(fields)
    collectChunkInList(JSON_CHUNKS, mappedChunk)


def deep_merge_dicts(original, incoming):
    """ Traverse paths of two dicts and only merge once these diverge taking only the leaves """
    for key in incoming:
        if key in original:
            if isinstance(original[key], dict) and isinstance(incoming[key], dict):
                deep_merge_dicts(original[key], incoming[key])
            else:
                original[key] = incoming[key]
        else:
            original[key] = incoming[key]


def intersectJsons(original, sanitized):
    """
        one = {a: {b: {c: c}}} <= Extracted from i18nt.('a.b.c')
        two = {a: {b: {c: "Hello"}}} <= Extracted from dirty translations.js file

        result = {a: {b: {c: "Hello"}}}
    """
    return {x: original[x] for x in original if x in sanitized}


if __name__ == "__main__":
    try:
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
            remapLineToDict(chunk)

        for chunk in JSON_CHUNKS:
            deep_merge_dicts(SANITIZED_JSON, chunk)

        with open(DIRTY_JSON_PATH, 'r') as json_file:
            dirtyJSON = json.load(json_file)
            intersectedDict = intersectJsons(dirtyJSON, SANITIZED_JSON)

        currentDate = str(datetime.datetime.now())
        filename = FINAL_DICTS_PATH + currentDate
        makedirs(path.dirname(filename), exist_ok=True)

        with open(filename, "w") as file:
            file.write(str(intersectedDict))

        print(f"\nSuccessfully sanitized i18n occurrences recursively"
              f" from {ROOT_PATH} and {DIRTY_JSON_PATH}"
              f"\nwith {len(ERROR_FILENAMES)} unabled to open files:"
              f" {ERROR_FILENAMES}\n")
    except Exception as error:
        print(f"\nSomething went terribly wrong {error}\n")
