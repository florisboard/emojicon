# emojicon
Preprocessing of Unicode Emoji definitions and annotations for FlorisBoard

Unicode provides the CLDR repository (https://github.com/unicode-org/cldr), which is used
by this tool to parse and build the necessary emoji mappings for the emoji palette within
the keyboard UI. All files within this project (source and data) are expected to be properly
encoded in UTF-8.

This project is structured in the following:
```
cldr/           Git submodule of the Unicode CLDR repository, checked out on a specific
                release, mostly the latest stable release.
prebuilt/       Pre-built emoji mapping files, which are then included in the main FlorisBoard
                repository (https://github.com/florisboard/florisboard) as a git submodule.
src/            The Python source code of the Emojicon tool.
```

To use this tool, make sure you have Python 3.10 or newer installed in your system and that you
ran `git submodule update --init --recursive` to initialize the git submodule.
