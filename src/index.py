"""
    Main entrypoint.

    1. Traverse ROOT_PATH recursively to find all occurrences of the i18n.t() call
    2. Extract 'settings.account.dummy' from i18.t('settings.account.dummy')
    3. Convert 'settings.account.dummy' to {settings: {account: {dummy: dummy }}}
    4. Convert single dicts into a global sanitized dict with deepMergeDicts
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
    match = re.search(I18N_REGEX, line)
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


def remapFieldsToDict(fields):
    """ Convert editProduct.genre.error recursively to {editProduct: {genre: {error: error}}}
        In order to reconstruct true dict skeleton. Leaf value will be replaced after
    """
    if len(fields) > 1:
        callback = remapFieldsToDict(fields[1:])
        return {fields[0]: callback}
    return {fields[0]: fields[0]}


def remapLineToDict(line):
    """ Convert 'editProduct.genre.error' to {editProduct: {genre: {error: error}}} """
    fields = convertStrippedChunkIntoList(line)

    mappedChunk = remapFieldsToDict(fields)
    collectChunkInList(JSON_CHUNKS, mappedChunk)


def checkValueIsDictionary(object, key):
    return isinstance(object[key], dict)


def deepMergeDicts(original, incoming):
    """ Traverse paths of two dicts and only merge once these diverge taking only the leaves """
    for key in incoming:
        if key in original:
            if checkValueIsDictionary(original, key) and checkValueIsDictionary(incoming, key):
                deepMergeDicts(original[key], incoming[key])
            else:
                original[key] = incoming[key]
        else:
            original[key] = incoming[key]


def checkDictionaryHasMoreThanOneValue(sanitized):
    return len(list(sanitized.values())) >= 1


def checkValueIsNotADictionary(sanitized):
    return not isinstance(list(sanitized.values())[0], dict)


def intersectDictionaries(sanitized, dirty):
    if checkDictionaryHasMoreThanOneValue(sanitized) and checkValueIsNotADictionary(sanitized):
        for key in sanitized:
            if key in dirty:
                sanitized[key] = dirty[key]
    else:
        for key in sanitized:
            if key in dirty:
                if checkValueIsDictionary(sanitized, key) and checkValueIsDictionary(dirty, key):
                    intersectDictionaries(sanitized[key], dirty[key])


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
            deepMergeDicts(SANITIZED_JSON, chunk)

        with open(DIRTY_JSON_PATH, 'r') as json_file:
            dirtyJSON = json.load(json_file)
            intersectDictionaries(SANITIZED_JSON, dirtyJSON)

        currentDate = str(datetime.datetime.now())
        filename = FINAL_DICTS_PATH + currentDate
        makedirs(path.dirname(filename), exist_ok=True)

        with open(filename, "w") as file:
            file.write(str(SANITIZED_JSON))

        print(f"\nSuccessfully sanitized i18n occurrences recursively"
              f" from {ROOT_PATH} and {DIRTY_JSON_PATH}"
              f"\nwith {len(ERROR_FILENAMES)} unabled to open files:"
              f" {ERROR_FILENAMES}\n")
    except Exception as error:
        print(f"\nSomething went terribly wrong {error}\n")
