#!/usr/bin/env python3
# encoding: utf-8

import io
import os
import shutil
import subprocess
import sys

from src.cldr_annotations import CldrAnnotationMapping, parse_cldr_annotation_dir, parse_cldr_annotation_file
from src.emoji import parse_emoji_test_file, write_emoji_data_file

BUILD_PATH = "build"
CLDR_PATH = f"{BUILD_PATH}/cldr"
CLDR_VERSION = "44.1" # write version in format major or major.minor

ANNOTATIONS_DIR_PATH = f"{CLDR_PATH}/common/annotations"
ANNOTATIONS_DERIVED_DIR_PATH = f"{CLDR_PATH}/common/annotationsDerived"
EMOJI_TEST_FILE_PATH = f"{CLDR_PATH}/tools/cldr-code/src/main/resources/org/unicode/cldr/util/data/emoji/emoji-test.txt"

EMOJI_ASSETS_OUTPUT_DIR_PATH = "prebuilt/emoji-{version}"
LANG_CODE_ROOT = "root"


def download_cldr(version: str):
    version_git = version.replace(".", "-")
    os.makedirs(BUILD_PATH, exist_ok=True)
    if os.path.exists(f"{BUILD_PATH}/release-{version_git}.tar.gz"):
        print(f"CLDR release {version} already downloaded")
    else:
        print(f"Downloading CLDR release {version}")
        subprocess.run(["wget", "-q", "--show-progress", f"https://github.com/unicode-org/cldr/archive/refs/tags/release-{version_git}.tar.gz", "-P", BUILD_PATH])
    if os.path.exists(CLDR_PATH):
        shutil.rmtree(CLDR_PATH)
    os.makedirs(CLDR_PATH, exist_ok=True)
    print(f"Extracting CLDR release {version} into {CLDR_PATH}")
    subprocess.run(["tar", "-xf", f"{BUILD_PATH}/release-{version_git}.tar.gz", "-C", CLDR_PATH, "--strip-components=1"])


def main(argv: list[str]):
    action = argv[1] if len(argv) > 1 else "help"

    match action:
        case "help" | "--help":
            with io.open("README.md", mode="r", encoding="utf-8") as f_readme:
                for line in f_readme.readlines():
                    print(line, end="")
        case "build":
            download_cldr(CLDR_VERSION)
            lang_code = argv[2] if len(argv) > 2 else LANG_CODE_ROOT
            emoji_data = parse_emoji_test_file(path=EMOJI_TEST_FILE_PATH)
            cldr_annotation_mapping: CldrAnnotationMapping
            if lang_code == LANG_CODE_ROOT:
                cldr_annotation_mapping = CldrAnnotationMapping()
            else:
                cldr_annotation_mapping = \
                    parse_cldr_annotation_file(f"{ANNOTATIONS_DIR_PATH}/{lang_code}.xml") | \
                    parse_cldr_annotation_file(f"{ANNOTATIONS_DERIVED_DIR_PATH}/{lang_code}.xml")
            out_dir = EMOJI_ASSETS_OUTPUT_DIR_PATH.format(version=CLDR_VERSION)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            out_path = f"{out_dir}/{lang_code}.txt"
            write_emoji_data_file(out_path, emoji_data, cldr_annotation_mapping)
        case "buildall":
            download_cldr(CLDR_VERSION)
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
            out_dir = EMOJI_ASSETS_OUTPUT_DIR_PATH.format(version=CLDR_VERSION)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            for lang_code, mapping in cldr_annotation_mappings.items():
                out_path = f"{out_dir}/{lang_code}.txt"
                if lang_code == LANG_CODE_ROOT:
                    write_emoji_data_file(out_path, emoji_data, CldrAnnotationMapping())
                else:
                    write_emoji_data_file(out_path, emoji_data, mapping)
        case "clean":
            shutil.rmtree("prebuilt")
        case _:
            print(f"[ERR] Unknown action: {action}")


if __name__ == "__main__":
    main(sys.argv)
