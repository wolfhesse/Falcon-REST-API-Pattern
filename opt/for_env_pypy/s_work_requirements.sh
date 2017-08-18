#!/usr/bin/env bash
pip install -r frozen.requirements.txt --upgrade
pip freeze >requirements.txt

echo comparing requirements files...
echo ==== anf
diff frozen.requirements.txt requirements.txt
echo ==== end
echo on-update todo: copy requirements.txt to frozen.requirements.txt
echo hint:  https://www.kennethreitz.org/essays/a-better-pip-workflow