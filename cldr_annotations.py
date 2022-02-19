#!/usr/bin/env python3.10
# encoding: utf-8

import io
import re
from dataclasses import dataclass, field

ANNOTATION_CP_NAME = re.compile(r'^\s*<annotation cp="(?P<cp>.+)" type="tts">(?P<cp_name>.+)</annotation>\s*$')
ANNOTATION_CP_KEYWORDS = re.compile(r'^\s*<annotation cp="(?P<cp>.+)">(?P<cp_keywords>.+)</annotation>\s*$')


@dataclass
class CldrAnnotationInfo:
    name: str = ""
    keywords: list[str] = field(default_factory=list)


def parse_annotations(path: str) -> dict[str, CldrAnnotationInfo]:
    annotations: dict[str, CldrAnnotationInfo] = dict()
    with io.open(path, mode="r", encoding="utf-8") as f_annotations:
        for line in f_annotations.readlines():
            match = re.match(ANNOTATION_CP_NAME, line)
            if match is not None:
                matches = match.groupdict()
                cp = matches["cp"]
                cp_name = matches["cp_name"]
                if cp not in annotations:
                    annotations[cp] = CldrAnnotationInfo()
                annotations.get(cp).name = cp_name
                continue
            match = re.match(ANNOTATION_CP_KEYWORDS, line)
            if match is not None:
                matches = match.groupdict()
                cp = matches["cp"]
                cp_keywords = matches["cp_keywords"]
                if cp not in annotations:
                    annotations[cp] = CldrAnnotationInfo()
                annotations.get(cp).keywords = list(map(str.strip, cp_keywords.split("|")))
                continue
    return annotations
