#!/usr/bin/env python3
# go.py
from os import system as s

import yaml

yml = yaml.safe_load(open("package.yml"))
s(f'''python3 {yml['package_name']}/{yml['package_name']}.py''')
