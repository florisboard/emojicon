#!/usr/bin/env python3
# encoding: utf-8

import io
import os.path
import re
from dataclasses import dataclass, field
from typing import Iterator

ANNOTATION_CP_NAME = re.compile(r'^\s*<annotation cp="(?P<cp>.+)" type="tts">(?P<cp_name>.+)</annotation>\s*$')
ANNOTATION_CP_KEYWORDS = re.compile(r'^\s*<annotation cp="(?P<cp>.+)">(?P<cp_keywords>.+)</annotation>\s*$')


@dataclass
class CldrAnnotationInfo:
    name: str = ""
    keywords: list[str] = field(default_factory=list)


CldrAnnotationMapping = dict[str, CldrAnnotationInfo]


def parse_cldr_annotation_file(path: str) -> CldrAnnotationMapping:
    assert os.path.exists(path), f"Specified path '{path}' does not exist!"
    assert os.path.isfile(path), f"Specified path '{path}' is not a file!"
    mapping: CldrAnnotationMapping = dict()
    with io.open(path, mode="r", encoding="utf-8") as f_annotations:
        for line in f_annotations.readlines():
            match = re.match(ANNOTATION_CP_NAME, line)
            if match is not None:
                matches = match.groupdict()
                cp = matches["cp"]
                cp_name = matches["cp_name"]
                if cp not in mapping:
                    mapping[cp] = CldrAnnotationInfo()
                mapping.get(cp).name = cp_name
                continue
            match = re.match(ANNOTATION_CP_KEYWORDS, line)
            if match is not None:
                matches = match.groupdict()
                cp = matches["cp"]
                cp_keywords = matches["cp_keywords"]
                if cp not in mapping:
                    mapping[cp] = CldrAnnotationInfo()
                mapping.get(cp).keywords = list(map(str.strip, cp_keywords.split("|")))
                continue
    return mapping


def parse_cldr_annotation_dir(path: dir) -> Iterator[tuple[str, CldrAnnotationMapping]]:
    assert os.path.exists(path), f"Specified path '{path}' does not exist!"
    assert os.path.isdir(path), f"Specified path '{path}' is not a directory!"
    for file_name in os.listdir(path):
        mapping = parse_cldr_annotation_file(path=f"{path}/{file_name}")
        lang_code = file_name.removesuffix(".xml")
        yield lang_code, mapping
