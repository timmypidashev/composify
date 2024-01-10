from setuptools import setup, find_packages
from pipfile import Pipfile
import os
import json

def get_version():
    init_py = os.path.join("src", "composify", "__init__.py")
    with open(init_py, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return eval(line.split('=')[1].strip())

def get_requirements():
    with open("Pipfile.lock", "r") as lock_file:
        lock_data = json.load(lock_file)

    requirements = []
    for package, details in lock_data["default"].items():
        requirements.append(f"{package}{details['version']}")

    return requirements

setup(
    name="composify",
    version=get_version(),
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "composify = composify:main",
        ],
    },
    install_requires=get_requirements(),
)
