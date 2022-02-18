#!/usr/bin/env python3.10
# encoding: utf-8

import os
from emoji import parse_emoji_test_file, write_emoji_data_file

EMOJI_TEST_FILE_PATH = "cldr/tools/cldr-code/src/main/resources/org/unicode/cldr/util/data/emoji/emoji-test.txt"

PATH_TMP = ".emojicon"
PATH_OUT = "prebuilt/assets/ime/media/emoji"


def main():
    emoji_data = parse_emoji_test_file(path=EMOJI_TEST_FILE_PATH)
    if not os.path.exists(PATH_TMP):
        os.mkdir(PATH_TMP)
    write_emoji_data_file(path=PATH_TMP + "/test.txt", emoji_data=emoji_data)


if __name__ == "__main__":
    main()
