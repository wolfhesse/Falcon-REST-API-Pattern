#!/usr/bin/env bash
cp requirements.txt frozen.requirements.txt

### pip install -r frozen.requirements.txt --upgrade
cat frozen.requirements.txt | awk -F= '{print $1}' | xargs -I {} pip install {} --upgrade


pip freeze >requirements.txt

echo comparing requirements files...
echo ==== anf
diff frozen.requirements.txt requirements.txt
echo ==== end
echo on-update todo: copy requirements.txt to frozen.requirements.txt
echo hint:  https://www.kennethreitz.org/essays/a-better-pip-workflow