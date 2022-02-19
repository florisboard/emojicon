#!/usr/bin/env python3
# encoding: utf-8

import io
import os
import shutil
import sys

from src.cldr_annotations import CldrAnnotationMapping, parse_cldr_annotation_dir, parse_cldr_annotation_file
from src.emoji import parse_emoji_test_file, write_emoji_data_file

ANNOTATIONS_DIR_PATH = "cldr/common/annotations"
ANNOTATIONS_DERIVED_DIR_PATH = "cldr/common/annotationsDerived"
EMOJI_TEST_FILE_PATH = "cldr/tools/cldr-code/src/main/resources/org/unicode/cldr/util/data/emoji/emoji-test.txt"

EMOJI_ASSETS_OUTPUT_DIR_PATH = "prebuilt/emoji"
LANG_CODE_ROOT = "root"


def main(argv: list[str]):
    action = argv[1] if len(argv) > 1 else "help"

    match action:
        case "help" | "--help":
            with io.open("README.md", mode="r", encoding="utf-8") as f_readme:
                for line in f_readme.readlines():
                    print(line, end="")
        case "build":
            lang_code = argv[2] if len(argv) > 2 else LANG_CODE_ROOT
            emoji_data = parse_emoji_test_file(path=EMOJI_TEST_FILE_PATH)
            cldr_annotation_mapping: CldrAnnotationMapping
            if lang_code == LANG_CODE_ROOT:
                cldr_annotation_mapping = CldrAnnotationMapping()
            else:
                cldr_annotation_mapping = \
                    parse_cldr_annotation_file(f"{ANNOTATIONS_DIR_PATH}/{lang_code}.xml") | \
                    parse_cldr_annotation_file(f"{ANNOTATIONS_DERIVED_DIR_PATH}/{lang_code}.xml")
            if not os.path.exists(EMOJI_ASSETS_OUTPUT_DIR_PATH):
                os.makedirs(EMOJI_ASSETS_OUTPUT_DIR_PATH)
            out_path = f"{EMOJI_ASSETS_OUTPUT_DIR_PATH}/{lang_code}.txt"
            write_emoji_data_file(out_path, emoji_data, cldr_annotation_mapping)
        case "buildall":
            emoji_data = parse_emoji_test_file(path=EMOJI_TEST_FILE_PATH)
            cldr_annotation_mappings: dict[str, CldrAnnotationMapping] = dict()
            cldr_annotation_mappings[LANG_CODE_ROOT] = CldrAnnotationMapping()  # empty mapping for root
            for lang_code, mapping in parse_cldr_annotation_dir(ANNOTATIONS_DIR_PATH):
                if lang_code not in cldr_annotation_mappings:
                    cldr_annotation_mappings[lang_code] = CldrAnnotationMapping()
                cldr_annotation_mappings[lang_code] |= mapping
            for lang_code, mapping in parse_cldr_annotation_dir(ANNOTATIONS_DERIVED_DIR_PATH):
                if lang_code not in cldr_annotation_mappings:
                    cldr_annotation_mappings[lang_code] = CldrAnnotationMapping()
                cldr_annotation_mappings[lang_code] |= mapping
            if not os.path.exists(EMOJI_ASSETS_OUTPUT_DIR_PATH):
                os.makedirs(EMOJI_ASSETS_OUTPUT_DIR_PATH)
            for lang_code, mapping in cldr_annotation_mappings.items():
                out_path = f"{EMOJI_ASSETS_OUTPUT_DIR_PATH}/{lang_code}.txt"
                write_emoji_data_file(out_path, emoji_data, mapping)
        case "clean":
            shutil.rmtree("prebuilt")
        case _:
            print(f"[ERR] Unknown action: {action}")


if __name__ == "__main__":
    main(sys.argv)
