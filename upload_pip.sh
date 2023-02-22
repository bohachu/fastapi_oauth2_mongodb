python setup.py sdist bdist_wheel
twine upload dist/*.tar.gz dist/*.whl
