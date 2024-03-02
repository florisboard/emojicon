# emojicon
Preprocessing of Unicode Emoji definitions and annotations for FlorisBoard

Unicode provides the CLDR repository (https://github.com/unicode-org/cldr), which is used
by this tool to parse and build the necessary emoji mappings for the emoji palette within
the keyboard UI. All files within this project (source and data) are expected to be properly
encoded in UTF-8.

## Usage

`./emojicon.py <action> [<options...>]`

To use this tool, make sure you have Python 3.10 or newer installed in your system.

### Actions

```
build <lang_code>   Builds the emoji mapping file for specified language. If no language code
                    is specified or 'root' is passed, all names and keywords will be left empty
                    and the generated file name is 'root.txt' in the output dir.
buildall            Builds the emoji mapping files for all langugaes including root.
clean               Removes the output directory and all built files.
help                Shows this help message.
```

## Project info

This project is structured in the following:

```
cldr/               Git submodule of the Unicode CLDR repository, checked out on a specific
                    release, mostly the latest stable release.
prebuilt/           Pre-built emoji mapping files, which are intended for usage in the main
                    FlorisBoard repository (https://github.com/florisboard/florisboard), for
                    now only root.txt though. (Usage of names and keywords planned later)
src/                The Python source code of the Emojicon tool.
```

## License

```
Copyright 2022-2024 Patrick Goldinger

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
