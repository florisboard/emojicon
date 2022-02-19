#!/usr/bin/env python3.10
# encoding: utf-8

from __future__ import annotations
from dataclasses import dataclass, field
import io

from cldr_annotations import CldrAnnotationInfo

GROUPS = {
    "smileys_emotion": "Smileys & Emotion",
    "people_body": "People & Body",
    "animals_nature": "Animals & Nature",
    "food_drink": "Food & Drink",
    "travel_places": "Travel & Places",
    "activities": "Activities",
    "objects": "Objects",
    "symbols": "Symbols",
    "flags": "Flags",
}

COMMENT_IDENTIFIER = "#"
GROUP_IDENTIFIER = "# group:"
EOF_IDENTIFIER = "#EOF"

GROUP_COMPONENT = "component"
FULLY_QUALIFIED = "fully-qualified"

VARIATIONS = {
    "light_skin_tone": 0x1F3FB,
    "medium_light_skin_tone": 0x1F3FC,
    "medium_skin_tone": 0x1F3FD,
    "medium_dark_skin_tone": 0x1F3FE,
    "dark_skin_tone": 0x1F3FF,
    "red_hair": 0x1F9B0,
    "curly_hair": 0x1F9B1,
    "white_hair": 0x1F9B2,
    "bald": 0x1F9B3,
}

SPECIAL_CP = 0xFE0F


@dataclass
class Emoji:
    qualified: str
    unqualified: str

    @staticmethod
    def from_code_points(code_points: list[int]) -> Emoji:
        return Emoji(
            qualified="".join(map(lambda cp: chr(cp), code_points)),
            unqualified="".join(map(lambda cp: chr(cp), filter(lambda cp: cp != SPECIAL_CP, code_points))),
        )

    def serialize(self, info: CldrAnnotationInfo | None = None) -> str:
        name = info.name if info is not None else ""
        keywords = "|".join(info.keywords) if info is not None else ""
        return f"{self.qualified};{name};{keywords}"


@dataclass
class EmojiSet:
    base: Emoji
    variations: list[Emoji] = field(default_factory=list)

    def serialize(self, cldr_annotations: dict[str, CldrAnnotationInfo]) -> str:
        ret = self.base.serialize(cldr_annotations.get(self.base.unqualified)) + "\n"
        for variation in self.variations:
            ret += "\t" + variation.serialize(cldr_annotations.get(variation.unqualified)) + "\n"
        return ret


def find_group_id(group_name: str) -> str | None:
    for id, name in GROUPS.items():
        if name == group_name:
            return id
    return None


def make_stats(data_path: str):
    with io.open(data_path, encoding="utf-8") as f_data:
        for line in f_data.readlines():
            if line.startswith("# group: "):
                print(line, end="")


def parse_emoji_test_file(path: str) -> dict[str, list[EmojiSet]]:
    emoji_data: dict[str, list[EmojiSet]] = dict()
    for group_id in GROUPS.keys():
        emoji_data[group_id] = []
    current_group_id = None
    with io.open(path, encoding="utf-8") as f_emoji_test:
        for line in f_emoji_test.readlines():
            if line.startswith(COMMENT_IDENTIFIER):
                # Comment line
                if line.startswith(GROUP_IDENTIFIER):
                    group_name = line.removeprefix(GROUP_IDENTIFIER).strip()
                    if group_name.lower() == GROUP_COMPONENT:
                        current_group_id = None
                    else:
                        current_group_id = find_group_id(group_name)
                elif line.startswith(EOF_IDENTIFIER):
                    break
                else:
                    # Ignore comment line
                    pass
            elif len(line.strip()) == 0 or current_group_id is None:
                # Empty line or no current group id specified
                continue
            else:
                # Assume it is a data line
                try:
                    cp_string, qualification = list(map(str.strip, line.split("#")[0].split(";")))
                    assert qualification == FULLY_QUALIFIED
                    cp_int = list(map(lambda s: int(s, base=16), cp_string.split(" ")))
                    assert len(cp_int) > 0
                    emoji = Emoji.from_code_points(cp_int)
                    if len(cp_int) > 1:
                        if cp_int[1] in VARIATIONS.values():
                            emoji_data[current_group_id][-1].variations.append(emoji)
                        else:
                            emoji_data[current_group_id].append(EmojiSet(base=emoji))
                    else:
                        emoji_data[current_group_id].append(EmojiSet(base=emoji))
                except AssertionError:
                    pass
    return emoji_data


def write_emoji_data_file(
    path: str,
    emoji_data: dict[str, list[EmojiSet]],
    cldr_annotations: dict[str, CldrAnnotationInfo],
):
    with io.open(path, "w", encoding="utf-8") as f_emoji_data:
        for group_id, emoji_sets in emoji_data.items():
            f_emoji_data.write(f"[{group_id}]\n")
            for emoji_set in emoji_sets:
                f_emoji_data.write(emoji_set.serialize(cldr_annotations))
            f_emoji_data.write("\n")
