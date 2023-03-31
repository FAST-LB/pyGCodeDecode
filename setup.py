# -*- coding: utf-8 -*-
"""Setup file."""
import platform
from setuptools import setup, find_packages

# if platform.python_version_tuple()[:2] == ("2", "7"):
#     requirements = [
#         "numpy",
#     ]
# else:
#     requirements = [
#         "numpy",
#         "matplotlib",
#         "typing",
#         "timeit",
#     ]

requirements = [
        "numpy",
        "matplotlib",
        "typing",
        # "timeit",
    ]

setup(
    name="pyGCodeDecode",
    internal_name="pygcodedecode",
    version="0.0.1",
    author="Jonathan Knirsch, Felix Froelich, Lukas Hof",
    author_email="felix.froelich@kit.edu",
    description="tbd",
    url="https://git.scc.kit.edu/FAST-LT/additive-manufacturing/pygcodedecode",
    #     license="MIT",
    #     package_dir={"": "src"},
    packages=find_packages(),
    install_requires=requirements,
)
