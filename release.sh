#!/usr/bin/env bash

#####################################################
#  command to create egg_info:
#              python setup.py egg_info
#  Register in https://pypi.python.org/pypi?%3Aaction=submit_form
######################################################

# Step 1, Remove old dist files
rm -rf ./dist/*

# Step 2, Build deploy files
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*