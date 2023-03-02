#!/usr/bin/env python3
# go.py
import os
from os import system as s

import yaml

os.environ['PYTHONPATH'] = '.'

s(f'''python3 -m pip install -r requirements.txt''')
yml = yaml.safe_load(open("package.yml"))
s(f'''python3 {yml['package_name']}/main.py''')
