#!/usr/bin/env python3.10
# encoding: utf-8

import os
from emoji import parse_emoji_test_file, write_emoji_data_file
from cldr_annotations import parse_annotations

EMOJI_TEST_FILE_PATH = "cldr/tools/cldr-code/src/main/resources/org/unicode/cldr/util/data/emoji/emoji-test.txt"
ANNOTATIONS_EN_PATH = "cldr/common/annotations/en.xml"
ANNOTATIONS_DERIVED_EN_PATH = "cldr/common/annotationsDerived/en.xml"

PATH_TMP = ".emojicon"
PATH_OUT = "prebuilt/assets/ime/media/emoji"


def main():
    emoji_data = parse_emoji_test_file(path=EMOJI_TEST_FILE_PATH)
    cldr_annotations = parse_annotations(path=ANNOTATIONS_EN_PATH) | parse_annotations(path=ANNOTATIONS_DERIVED_EN_PATH)
    if not os.path.exists(PATH_TMP):
        os.mkdir(PATH_TMP)
    write_emoji_data_file(path=PATH_TMP + "/test.txt", emoji_data=emoji_data, cldr_annotations=cldr_annotations)


if __name__ == "__main__":
    main()
