# !/usr/bin/env python3
# upload_pip.py
from os import system as s

import yaml

yml = yaml.safe_load(open("package.yml"))

s("rm -fr dist")
s("python setup.py sdist bdist_wheel")
s("twine upload dist/*.tar.gz dist/*.whl")
s(f"python3 -m pip install -U {yml['package_name']}")
s(f"python3 -m {yml['package_name']}")
