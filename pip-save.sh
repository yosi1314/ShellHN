#/bin/sh
pip install $1 && pip freeze | grep $1 >> requirements.txt